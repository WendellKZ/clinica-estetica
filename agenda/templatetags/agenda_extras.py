from __future__ import annotations

from django import template

register = template.Library()


def _norm_status(value) -> str:
    if value is None:
        return ""
    s = str(value).strip().upper()
    # common aliases
    if s in {"REALIZADO", "ATENDIDO", "FINALIZADO", "CONCLUIDO", "CONCLUÍDO"}:
        return "REALIZADO"
    if s in {"FALTOU", "NAO_COMPARECEU", "NÃO COMPARECEU", "NO_SHOW", "NO-SHOW"}:
        return "FALTOU"
    return s


def _status_to_class(status: str) -> str:
    s = _norm_status(status)
    if s == "CANCELADO":
        return "appt-status-cancelado"
    if s == "CONFIRMADO":
        return "appt-status-confirmado"
    if s == "REALIZADO":
        return "appt-status-realizado"
    if s == "FALTOU":
        return "appt-status-faltou"
    # default
    return "appt-status-marcado"


@register.filter(name="agenda_bar_class")
def agenda_bar_class(status) -> str:
    """CSS class applied on the appointment card wrapper."""
    return _status_to_class(status)


@register.filter(name="agenda_badge_class")
def agenda_badge_class(status) -> str:
    """CSS class applied on the status badge.

    We reuse the same class as the card wrapper so the CSS variants work.
    """
    return _status_to_class(status)
