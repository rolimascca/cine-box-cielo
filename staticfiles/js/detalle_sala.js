console.log("👋 ¡Hola! Soy el robot JavaScript y estoy funcionando!");

document.addEventListener('DOMContentLoaded', function () {
    // Elementos del DOM
    const radios = document.querySelectorAll('.horario-radio');
    const mensajeSeleccionado = document.getElementById('mensajeSeleccionado');
    const horarioIdInput = document.getElementById('horario_id_input');

    // Verificar si hay elementos
    if (!radios.length || !mensajeSeleccionado || !horarioIdInput) {
        console.warn("⚠️ No se encontraron todos los elementos necesarios");
        return;
    }

    // Función para verificar disponibilidad del horario
    async function verificarHorario(hora, salaSlug) {
        try {
            const response = await fetch("{% url 'verificar_horario' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({
                    horario: hora,
                    sala_slug: "{{ sala.slug }}"
                })
            });

            return await response.json();
        } catch (error) {
            console.error("❌ Error al verificar el horario:", error);
            return { ocupado: false }; // Por defecto asumimos que está disponible
        }
    }

    // Configurar eventos para cada radio button
    radios.forEach(radio => {
        console.log("⏰ Horario disponible:", radio.value);

        radio.addEventListener('change', async function () {
            if (!this.checked) return;

            const horarioSeleccionado = this.value;
            const [horarioId, hora] = horarioSeleccionado.split('|');

            // Limpiar selecciones anteriores
            document.querySelectorAll('.horario-disponible, .horario-btn').forEach(el => {
                el.classList.remove('seleccionado', 'active');
            });

            // Resaltar selección actual
            const label = this.closest('.horario-item') ?
                this.nextElementSibling :
                this.parentElement;
            label.classList.add('seleccionado', 'active');

            // Actualizar mensaje e input oculto
            mensajeSeleccionado.textContent = `Has seleccionado el horario: ${hora}`;
            horarioIdInput.value = horarioId;

            // Verificar disponibilidad
            const resultado = await verificarHorario(hora, "{{ sala.slug }}");

            if (resultado.ocupado) {
                alert("⚠️ El horario seleccionado ya está ocupado. Por favor, elige otro.");
                this.checked = false;
                label.classList.remove('seleccionado', 'active');
                mensajeSeleccionado.textContent = '';
                horarioIdInput.value = '';
            }
        });
    });

    // Actualizar automáticamente cada 5 minutos
    const intervaloActualizacion = setInterval(() => {
        console.log("🔄 Actualizando horarios...");
        window.location.reload();
    }, 300000); // 5 minutos

    // Limpiar intervalo si la página se cierra (buena práctica)
    window.addEventListener('beforeunload', () => {
        clearInterval(intervaloActualizacion);
    });
});