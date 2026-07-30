from pathlib import Path
from io import StringIO
from unittest.mock import patch

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.management import call_command
from django.test import Client, RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone


class HealthCheckTests(SimpleTestCase):
    def test_health_endpoint_is_public_and_reports_ok(self):
        response = Client().get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class BrandIdentityTests(TestCase):
    def test_login_uses_elisangela_brand_image(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "logo-elisangela-identidade.png")
        self.assertContains(response, "Elisângela Barbosa Estética")
        self.assertNotContains(response, "Sistema Clínica")


class DeploymentConfigurationTests(SimpleTestCase):
    def test_render_uses_dedicated_health_check_and_https_security(self):
        render_config = (
            Path(__file__).resolve().parents[1] / "render.yaml"
        ).read_text(encoding="utf-8")

        self.assertIn("healthCheckPath: /health/", render_config)
        self.assertIn("key: SECURE_SSL_REDIRECT", render_config)
        self.assertIn("key: SECURE_HSTS_SECONDS", render_config)

    def test_authentication_middleware_is_not_registered_twice(self):
        middleware = "django.contrib.auth.middleware.AuthenticationMiddleware"

        self.assertEqual(settings.MIDDLEWARE.count(middleware), 1)

    def test_whitenoise_serves_collected_static_files_in_production(self):
        security = settings.MIDDLEWARE.index(
            "django.middleware.security.SecurityMiddleware"
        )
        whitenoise = settings.MIDDLEWARE.index(
            "whitenoise.middleware.WhiteNoiseMiddleware"
        )

        self.assertEqual(whitenoise, security + 1)


class BootstrapAdminCommandTests(TestCase):
    @patch.dict(
        "os.environ",
        {
            "INITIAL_ADMIN_USERNAME": "admin_teste",
            "INITIAL_ADMIN_EMAIL": "admin@teste.com",
            "INITIAL_ADMIN_PASSWORD": "SenhaTemporaria#7284",
        },
    )
    def test_creates_superuser_from_environment_only_once(self):
        output = StringIO()

        call_command("bootstrap_admin", stdout=output)
        call_command("bootstrap_admin", stdout=output)

        users = get_user_model().objects.filter(username="admin_teste")
        self.assertEqual(users.count(), 1)
        user = users.get()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password("SenhaTemporaria#7284"))


class PermissionsModuleTests(SimpleTestCase):
    def test_deny_redirects_to_default_route(self):
        from core.permissions import deny

        request = RequestFactory().get("/")
        request.session = {}
        request._messages = FallbackStorage(request)

        response = deny(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/agenda/")


class AuthenticationAndAuthorizationTests(TestCase):
    def test_anonymous_user_is_redirected_from_business_pages(self):
        protected_urls = [
            reverse("dashboard"),
            reverse("clientes_lista"),
            reverse("agenda:agenda_lista"),
            reverse("loja:venda_nova"),
            reverse("financeiro_lista"),
            reverse("usuarios:usuario_lista"),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/login/", response.url)

    def test_non_admin_cannot_access_user_management(self):
        user = get_user_model().objects.create_user(
            username="profissional", password="senha-forte-123"
        )
        self.client.force_login(user)

        response = self.client.get(reverse("usuarios:usuario_lista"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)


class EmpresasModuleTests(TestCase):
    def test_empresas_helpers_import_and_create_default_empresa(self):
        from empresas.context_processors import empresa_context
        from empresas.models import Empresa
        from empresas.utils import ensure_default_empresa

        empresa = ensure_default_empresa()

        self.assertEqual(Empresa.objects.count(), 1)
        self.assertEqual(empresa.nome, "Minha Clinica")

        request = RequestFactory().get("/")
        request.session = {}
        context = empresa_context(request)
        self.assertEqual(context["current_empresa"], empresa)


class MainFlowSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="codex",
            password="senha-forte-123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.user)

    def test_authenticated_main_pages_render(self):
        from clientes.models import Cliente
        from loja.models import Produto

        cliente = Cliente.objects.create(nome="Cliente Smoke", telefone="11999999999")
        produto = Produto.objects.create(
            nome="Produto Smoke",
            sku="SMK",
            custo="10.00",
            preco_venda="25.00",
            estoque_atual=5,
            ativo=True,
        )

        pages = [
            "/",
            reverse("clientes_lista"),
            reverse("clientes_novo"),
            reverse("agenda:agenda_lista"),
            reverse("agenda:agenda_novo"),
            reverse("loja:venda_nova"),
            reverse("loja:produtos_lista"),
            reverse("loja:produto_json", args=[produto.pk]),
            reverse("financeiro_lista"),
            reverse("financeiro_novo"),
            reverse("servicos:servico_lista"),
            reverse("servicos:servico_novo"),
            reverse("produtos:produto_list"),
            reverse("produtos:produto_create"),
            reverse("usuarios:usuario_lista"),
            reverse("clientes_editar", args=[cliente.pk]),
        ]

        for url in pages:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_cliente_agenda_venda_financeiro_flow_executes(self):
        from agenda.models import Agendamento, Servico
        from clientes.models import Cliente
        from financeiro.models import LancamentoFinanceiro
        from loja.models import Produto, Venda

        response = self.client.post(
            reverse("clientes_novo"),
            {
                "nome": "Maria Smoke",
                "telefone": "11988887777",
                "email": "maria@example.com",
                "observacoes": "Teste automatizado",
            },
        )
        self.assertEqual(response.status_code, 302)
        cliente = Cliente.objects.get(nome="Maria Smoke")

        servico = Servico.objects.create(nome="Limpeza de pele", preco="120.00", duracao_minutos=60)
        inicio = timezone.localtime() + timezone.timedelta(days=1)
        fim = inicio + timezone.timedelta(hours=1)
        response = self.client.post(
            reverse("agenda:agenda_novo"),
            {
                "cliente": cliente.pk,
                "profissional": self.user.pk,
                "servico": servico.pk,
                "inicio": inicio.strftime("%Y-%m-%dT%H:%M"),
                "fim": fim.strftime("%Y-%m-%dT%H:%M"),
                "status": "MARCADO",
                "observacoes": "Criado no smoke test",
                "duracao_min": "60",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Agendamento.objects.filter(cliente=cliente, servico=servico).exists())

        produto = Produto.objects.create(
            nome="Creme Smoke",
            custo="8.00",
            preco_venda="20.00",
            estoque_atual=3,
            ativo=True,
        )
        response = self.client.post(
            reverse("loja:venda_nova"),
            {
                "cliente": cliente.pk,
                "forma_pagamento": "PIX",
                "observacao": "Venda smoke",
            },
        )
        self.assertEqual(response.status_code, 302)
        venda = Venda.objects.latest("id")

        response = self.client.post(
            reverse("loja:venda_detalhe", args=[venda.pk]),
            {
                "add_item": "1",
                "produto": produto.pk,
                "quantidade": "2",
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse("loja:venda_finalizar", args=[venda.pk]))
        self.assertEqual(response.status_code, 302)
        produto.refresh_from_db()
        venda.refresh_from_db()
        self.assertEqual(produto.estoque_atual, 1)
        self.assertEqual(venda.total, 40)
        self.assertTrue(LancamentoFinanceiro.objects.filter(venda=venda, valor=40).exists())

    def test_finalizing_same_sale_twice_does_not_deduct_stock_twice(self):
        from financeiro.models import LancamentoFinanceiro
        from loja.models import Produto, Venda, VendaItem

        produto = Produto.objects.create(
            nome="Produto idempotente",
            custo="5.00",
            preco_venda="15.00",
            estoque_atual=5,
            ativo=True,
        )
        produto.refresh_from_db()
        venda = Venda.objects.create(forma_pagamento="PIX")
        VendaItem.objects.create(
            venda=venda,
            produto=produto,
            quantidade=2,
            preco_unitario=produto.preco_venda,
            custo_unitario=produto.custo,
        )

        url = reverse("loja:venda_finalizar", args=[venda.pk])
        self.client.post(url)
        self.client.post(url)

        produto.refresh_from_db()
        self.assertEqual(produto.estoque_atual, 3)
        self.assertEqual(LancamentoFinanceiro.objects.filter(venda=venda).count(), 1)

    def test_agenda_status_rejects_value_outside_model_choices(self):
        from agenda.models import Agendamento, Servico
        from clientes.models import Cliente

        cliente = Cliente.objects.create(nome="Cliente status")
        servico = Servico.objects.create(
            nome="Serviço status", preco="50.00", duracao_minutos=30
        )
        inicio = timezone.now() + timezone.timedelta(days=1)
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            profissional=self.user,
            servico=servico,
            inicio=inicio,
            fim=inicio + timezone.timedelta(minutes=30),
        )

        response = self.client.post(
            f"/agenda/{agendamento.pk}/status/INVENTADO/",
        )

        agendamento.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(agendamento.status, "MARCADO")

    def test_marking_appointment_realized_creates_attendance_and_finance_once(self):
        from agenda.models import Agendamento, Atendimento, Servico
        from clientes.models import Cliente
        from financeiro.models import LancamentoFinanceiro

        cliente = Cliente.objects.create(nome="Cliente realizado")
        servico = Servico.objects.create(
            nome="Procedimento realizado", preco="90.00", duracao_minutos=45
        )
        inicio = timezone.now()
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            profissional=self.user,
            servico=servico,
            inicio=inicio,
            fim=inicio + timezone.timedelta(minutes=45),
        )
        url = f"/agenda/{agendamento.pk}/status/REALIZADO/"

        first_response = self.client.post(url)
        second_response = self.client.post(url)

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(Atendimento.objects.filter(agendamento=agendamento).count(), 1)
        self.assertEqual(
            LancamentoFinanceiro.objects.filter(
                agendamento=agendamento,
                origem="PROCEDIMENTO",
                tipo="ENTRADA",
            ).count(),
            1,
        )


class DashboardWeeklyAgendaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="agenda_admin",
            password="senha-forte-123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.user)

    def test_dashboard_groups_only_current_week_days_with_appointments(self):
        from agenda.models import Agendamento, Servico
        from clientes.models import Cliente

        today = timezone.localdate()
        monday = today - timezone.timedelta(days=today.weekday())
        cliente = Cliente.objects.create(nome="Cliente da semana")
        servico = Servico.objects.create(
            nome="Limpeza facial", preco="100.00", duracao_minutos=60
        )

        first_day = monday + timezone.timedelta(days=1)
        second_day = monday + timezone.timedelta(days=3)
        next_week = monday + timezone.timedelta(days=8)

        for appointment_day in (first_day, second_day, next_week):
            inicio = timezone.make_aware(
                timezone.datetime.combine(
                    appointment_day, timezone.datetime.min.time()
                ).replace(hour=10)
            )
            Agendamento.objects.create(
                cliente=cliente,
                profissional=self.user,
                servico=servico,
                inicio=inicio,
                fim=inicio + timezone.timedelta(hours=1),
                status="MARCADO",
            )

        response = self.client.get(reverse("dashboard"))

        groups = response.context["agenda_semana_dias"]
        self.assertEqual([group["data"] for group in groups], [first_day, second_day])
        self.assertTrue(all(group["agendamentos"] for group in groups))
        self.assertContains(response, "Agenda da semana")
        self.assertContains(response, "Cliente da semana", count=2)

    def test_dashboard_shows_empty_week_message(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.context["agenda_semana_dias"], [])
        self.assertContains(response, "Nenhum agendamento nesta semana")


class GuidedWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="wizard_admin",
            password="senha-forte-123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.user)

    def test_main_create_forms_render_guided_steps(self):
        urls = [
            reverse("clientes_novo"),
            reverse("loja:produto_novo"),
            reverse("loja:venda_nova"),
            reverse("servicos:servico_novo"),
            reverse("usuarios:usuario_novo"),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'data-wizard="true"')
                self.assertContains(response, 'class="wizard-progress"')
                self.assertContains(response, "Continuar")

    def test_global_layout_loads_natural_theme_and_wizard_assets(self):
        response = self.client.get(reverse("dashboard"))

        self.assertContains(response, "css/guided-workflows.css")
        self.assertContains(response, "js/guided-workflows.js")

    def test_sale_uses_contextual_header_and_side_step_layout(self):
        response = self.client.get(reverse("loja:venda_nova"))

        self.assertContains(response, 'class="top-header-title"')
        self.assertContains(response, "Nova venda", count=2)
        self.assertNotContains(response, '<div class="fs-5 fw-semibold text-dark">')
        self.assertContains(response, 'class="wizard-layout"')
        self.assertContains(response, 'class="wizard-sidebar"')

    def test_all_guided_forms_use_side_step_layout(self):
        urls = [
            reverse("clientes_novo"),
            reverse("loja:produto_novo"),
            reverse("servicos:servico_novo"),
            reverse("usuarios:usuario_novo"),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'class="wizard-layout"')
                self.assertContains(response, 'class="wizard-sidebar"')


class GuidedAppointmentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="agenda_wizard",
            password="senha-forte-123",
            is_staff=True,
        )
        self.client.force_login(self.user)

    @patch("agenda.views.timezone.localtime")
    def test_new_appointment_starts_five_minutes_ahead(self, mocked_localtime):
        fixed_now = timezone.make_aware(
            timezone.datetime(2026, 7, 30, 11, 38)
        )
        mocked_localtime.return_value = fixed_now

        response = self.client.get(reverse("agenda:agenda_novo"))

        form = response.context["form"]
        self.assertEqual(form.initial["inicio"], fixed_now + timezone.timedelta(minutes=5))
        self.assertEqual(form.initial["fim"], fixed_now + timezone.timedelta(minutes=65))

    def test_new_appointment_uses_four_guided_steps(self):
        response = self.client.get(reverse("agenda:agenda_novo"))

        self.assertContains(response, 'data-wizard="true"')
        self.assertContains(response, 'class="wizard-layout"')
        self.assertContains(response, 'class="wizard-sidebar"')
        self.assertContains(response, "1. Cliente")
        self.assertContains(response, "4. Conferir")
        self.assertContains(response, 'class="top-header-title"')
        self.assertContains(response, "Novo agendamento")
