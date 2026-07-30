(function () {
  document.documentElement.classList.remove("no-js");

  function fieldValue(field) {
    if (field.type === "checkbox") return field.checked ? "Sim" : "Não";
    if (field.tagName === "SELECT") {
      return Array.from(field.selectedOptions).map(function (option) {
        return option.text;
      }).filter(Boolean).join(", ") || "Não informado";
    }
    return field.value.trim() || "Não informado";
  }

  document.querySelectorAll('[data-wizard="true"]').forEach(function (form) {
    var steps = Array.from(form.querySelectorAll(".wizard-step"));
    var indicators = Array.from(form.querySelectorAll(".wizard-progress-item"));
    var current = 0;

    function fillSummary(step) {
      var summary = step.querySelector(".wizard-summary");
      if (!summary) return;
      summary.innerHTML = "";
      var fields = Array.from(form.querySelectorAll("[data-summary-label]"));
      if (!fields.length) {
        fields = Array.from(form.querySelectorAll("input, select, textarea")).filter(function (field) {
          return field.type !== "hidden" && field.type !== "password" && field.type !== "submit";
        });
      }
      fields.forEach(function (field) {
        var label = field.dataset.summaryLabel;
        if (!label && field.id) {
          var labelNode = form.querySelector('label[for="' + field.id + '"]');
          if (labelNode) label = labelNode.textContent.trim();
        }
        label = label || field.name;
        var row = document.createElement("div");
        row.className = "wizard-summary-row";
        row.innerHTML =
          '<span class="wizard-summary-label"></span><span class="wizard-summary-value"></span>';
        row.querySelector(".wizard-summary-label").textContent =
          label;
        row.querySelector(".wizard-summary-value").textContent = fieldValue(field);
        summary.appendChild(row);
      });
    }

    function show(index) {
      current = Math.max(0, Math.min(index, steps.length - 1));
      steps.forEach(function (step, stepIndex) {
        step.classList.toggle("is-active", stepIndex === current);
        step.hidden = stepIndex !== current;
      });
      indicators.forEach(function (indicator, indicatorIndex) {
        indicator.classList.toggle("is-active", indicatorIndex === current);
        indicator.classList.toggle("is-complete", indicatorIndex < current);
        if (indicatorIndex === current) indicator.setAttribute("aria-current", "step");
        else indicator.removeAttribute("aria-current");
      });
      fillSummary(steps[current]);
      var heading = steps[current].querySelector("h2, h3");
      if (heading) {
        heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
      }
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function validateStep() {
      var controls = Array.from(steps[current].querySelectorAll("input, select, textarea"));
      for (var i = 0; i < controls.length; i += 1) {
        if (!controls[i].checkValidity()) {
          controls[i].reportValidity();
          controls[i].focus();
          return false;
        }
      }
      return true;
    }

    form.addEventListener("click", function (event) {
      var next = event.target.closest(".wizard-next, [data-next]");
      var back = event.target.closest(".wizard-back, [data-back]");
      if (next) {
        event.preventDefault();
        if (validateStep()) show(current + 1);
      }
      if (back) {
        event.preventDefault();
        show(current - 1);
      }
    });

    var error = form.querySelector(".wizard-field-error, .errorlist");
    if (error) {
      var errorStep = error.closest(".wizard-step");
      var errorIndex = steps.indexOf(errorStep);
      show(errorIndex >= 0 ? errorIndex : 0);
    } else {
      show(0);
    }
  });
})();
