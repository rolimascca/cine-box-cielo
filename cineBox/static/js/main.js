/**
 * Clase para manejar la visibilidad de las contraseñas con animaciones
 */
class PasswordToggle {
    constructor(inputId, toggleId) {
        this.input = document.getElementById(inputId);
        this.toggle = document.getElementById(toggleId);
        this.initialize();
    }

    initialize() {
        if (this.toggle && this.input) {
            this.toggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleVisibility();
            });
        }
    }

    toggleVisibility() {
        const isPassword = this.input.type === 'password';

        // Animación de transición suave
        this.input.style.transition = 'all 0.3s ease';
        this.input.type = isPassword ? 'text' : 'password';

        // Animación del ícono
        const icon = this.toggle.querySelector('i');
        if (icon) {
            icon.style.transform = 'scale(0)';
            setTimeout(() => {
                icon.className = `fa fa-eye${isPassword ? '-slash' : ''}`;
                icon.style.transform = 'scale(1)';
            }, 150);
        }

        // Efecto de hover animado
        this.toggle.style.transform = 'scale(1)';
        setTimeout(() => {
            this.toggle.style.transform = 'scale(1.1)';
            setTimeout(() => {
                this.toggle.style.transform = 'scale(1)';
            }, 100);
        }, 50);
    }
}

/**
 * Clase para validar formularios con feedback visual
 */
class FormValidator {
    static validateEmail(email) {
        const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        this.animateValidation('id_email', isValid);
        return isValid;
    }

    static validatePassword(password) {
        const isValid = password.length >= 6;
        this.animateValidation('id_password1', isValid);
        return isValid;
    }

    static animateValidation(fieldId, isValid) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        field.style.transition = 'all 0.3s ease';
        field.style.boxShadow = isValid
            ? '0 0 10px rgba(46, 204, 113, 0.5)'
            : '0 0 10px rgba(231, 76, 60, 0.5)';

        setTimeout(() => {
            field.style.boxShadow = 'none';
        }, 1000);
    }

    static showError(message, element) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error animate__animated animate__shakeX';
        errorDiv.textContent = message;

        element.parentNode.insertBefore(errorDiv, element.nextSibling);

        setTimeout(() => {
            errorDiv.classList.add('animate__fadeOut');
            setTimeout(() => errorDiv.remove(), 500);
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar componentes con animaciones
    const passwordToggles = [
        new PasswordToggle('id_password1', 'register-password-toggle'),
        new PasswordToggle('id_password2', 'confirm-password-toggle')
    ];

    // Validación en tiempo real con animaciones
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        const fields = {
            email: document.getElementById('id_email'),
            password1: document.getElementById('id_password1'),
            password2: document.getElementById('id_password2')
        };

        // Animación al enfocar campos
        Object.values(fields).forEach(field => {
            field.addEventListener('focus', () => {
                field.style.transform = 'scale(1.02)';
                field.parentElement.style.transform = 'translateY(-2px)';
            });

            field.addEventListener('blur', () => {
                field.style.transform = 'scale(1)';
                field.parentElement.style.transform = 'translateY(0)';
            });
        });

        // Manejo de submit con animaciones
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Animación de carga
            const submitButton = registerForm.querySelector('button[type="submit"]');
            submitButton.innerHTML = '<div class="loader"></div> Procesando...';
            submitButton.disabled = true;

            // Validación animada
            const isValid = await validateForm();

            if (isValid) {
                // Animación de éxito
                submitButton.style.backgroundColor = '#2ecc71';
                setTimeout(() => registerForm.submit(), 1000);
            } else {
                // Animación de error
                submitButton.style.backgroundColor = '#e74c3c';
                setTimeout(() => {
                    submitButton.innerHTML = 'Regístrate';
                    submitButton.disabled = false;
                }, 1000);
            }
        });

        async function validateForm() {
            // Validaciones con animaciones
            const emailValid = FormValidator.validateEmail(fields.email.value);
            const passwordValid = FormValidator.validatePassword(fields.password1.value);
            const passwordsMatch = fields.password1.value === fields.password2.value;

            if (!emailValid) {
                FormValidator.showError('Email inválido', fields.email);
            }
            if (!passwordValid) {
                FormValidator.showError('Mínimo 6 caracteres', fields.password1);
            }
            if (!passwordsMatch) {
                FormValidator.showError('Las contraseñas no coinciden', fields.password2);
            }

            return emailValid && passwordValid && passwordsMatch;
        }
    }
});