# Política de Seguridad y Prevención de Fraudes — NovaPay SpA

**Versión:** 2.1  
**Aprobado por:** Comité de Seguridad de la Información  
**Fecha:** 10 de noviembre de 2025

## 1. Objetivo

Establecer los lineamientos, controles y procedimientos de seguridad de la información que NovaPay SpA implementa para proteger los activos digitales, datos de usuarios y la integridad de las operaciones financieras procesadas a través de la plataforma.

## 2. Alcance

Esta política aplica a todos los colaboradores de NovaPay, contratistas, proveedores con acceso a sistemas y usuarios de la plataforma. Cubre todos los sistemas, redes, aplicaciones, bases de datos y dispositivos utilizados en la operación.

## 3. Marco Normativo y Estándares

NovaPay alinea su gestión de seguridad con:
- **ISO/IEC 27001:2022** — Sistema de Gestión de Seguridad de la Información (certificación vigente desde marzo 2024).
- **PCI DSS v4.0** — Estándar de seguridad para datos de tarjetas de pago.
- **Ley 21.663** — Ley Marco sobre Ciberseguridad (Chile, 2024).
- **Circular CMF N° 3.800** — Gestión de riesgo operacional y tecnológico en entidades financieras.
- **NIST Cybersecurity Framework 2.0** — Marco de referencia para gestión de riesgos cibernéticos.

## 4. Arquitectura de Seguridad

### 4.1 Seguridad en Capas (Defense in Depth)

NovaPay implementa un modelo de seguridad en capas:

**Capa 1 — Perímetro:**
- Firewall de nueva generación (NGFW) con inspección de paquetes.
- WAF (Web Application Firewall) para protección contra OWASP Top 10.
- DDoS mitigation con capacidad de absorción de hasta 1 Tbps.
- CDN con geo-restricciones configurables.

**Capa 2 — Red:**
- Segmentación de red (VLANs) con microsegmentación para sistemas críticos.
- VPN site-to-site con cifrado IPSec para comunicaciones inter-datacenter.
- IDS/IPS (Intrusion Detection/Prevention System) con reglas actualizadas diariamente.
- Zero Trust Network Access (ZTNA) para acceso remoto de colaboradores.

**Capa 3 — Aplicación:**
- Desarrollo seguro (SDLC) con revisión de código obligatoria.
- SAST (Static Application Security Testing) integrado en CI/CD.
- DAST (Dynamic Application Security Testing) semanal.
- Dependency scanning para vulnerabilidades en librerías de terceros.
- API Gateway con rate limiting, autenticación OAuth 2.0 y validación de tokens JWT.

**Capa 4 — Datos:**
- Cifrado AES-256 para datos en reposo.
- TLS 1.3 para datos en tránsito.
- Tokenización de datos sensibles (números de tarjeta, RUT).
- Enmascaramiento de datos en ambientes de desarrollo y QA.
- Backups cifrados con retención de 90 días y pruebas de restauración mensuales.

### 4.2 Gestión de Identidades y Accesos (IAM)

- Principio de mínimo privilegio para todos los accesos.
- Autenticación multifactor (MFA) obligatoria para colaboradores.
- Revisión trimestral de permisos y accesos.
- Rotación de credenciales de servicio cada 90 días.
- Single Sign-On (SSO) con SAML 2.0 para aplicaciones corporativas.
- Logs de acceso centralizados con retención de 1 año.

## 5. Prevención de Fraudes

### 5.1 Sistema de Detección de Fraudes

NovaPay opera un motor de detección de fraudes en tiempo real que analiza cada transacción evaluando más de 200 variables, incluyendo:

- Monto y frecuencia de transacciones.
- Ubicación geográfica del dispositivo.
- Patrones de comportamiento del usuario (behavioral analytics).
- Dispositivo utilizado (device fingerprinting).
- Velocidad de operaciones sucesivas.
- Consistencia con el perfil histórico del usuario.

Las transacciones se clasifican en tres niveles de riesgo:
- **Bajo (score 0-30):** Aprobación automática.
- **Medio (score 31-70):** Aprobación con verificación adicional (OTP o biometría).
- **Alto (score 71-100):** Bloqueo automático y revisión manual por el equipo de fraudes.

### 5.2 Tipos de Fraude Monitoreados

- **Phishing:** Correos, SMS o sitios web que suplantan la identidad de NovaPay.
- **Account Takeover (ATO):** Acceso no autorizado a cuentas mediante credenciales robadas.
- **Fraude de identidad sintética:** Uso de datos combinados reales y ficticios para crear identidades falsas.
- **Card-not-present (CNP):** Uso fraudulento de datos de tarjetas en compras en línea.
- **Money muling:** Uso de cuentas de terceros para lavar fondos ilícitos.
- **Ingeniería social:** Manipulación psicológica para obtener información confidencial.

### 5.3 Procedimiento ante Incidentes de Fraude

1. **Detección:** El sistema automático o el usuario reporta la actividad sospechosa.
2. **Contención:** Bloqueo inmediato de la cuenta o tarjeta afectada.
3. **Investigación:** El equipo de fraudes analiza la transacción en un plazo máximo de 10 días hábiles.
4. **Resolución:** Si se confirma el fraude, se procede al reembolso y se reporta a la UAF si corresponde.
5. **Recuperación:** Se emiten nuevas credenciales y se refuerzan los controles de la cuenta.
6. **Lecciones aprendidas:** Se actualiza el motor de detección con los nuevos patrones identificados.

## 6. Gestión de Incidentes de Seguridad

### 6.1 Clasificación de Incidentes

| Severidad | Descripción | Tiempo de respuesta | Ejemplo |
|-----------|-------------|---------------------|---------|
| Crítica | Compromiso de datos masivo o interrupción total del servicio | 15 minutos | Brecha de datos, ransomware |
| Alta | Compromiso parcial o degradación significativa | 1 hora | Acceso no autorizado a sistema interno |
| Media | Incidente contenido sin impacto en usuarios | 4 horas | Malware detectado en estación de trabajo |
| Baja | Evento de seguridad menor | 24 horas | Intento de phishing bloqueado |

### 6.2 Equipo de Respuesta (CSIRT)

NovaPay cuenta con un equipo CSIRT (Computer Security Incident Response Team) de 8 personas, disponible 24/7 con rotación de turnos. El equipo incluye:
- 1 CISO (Chief Information Security Officer)
- 2 Analistas de seguridad senior
- 3 Analistas de seguridad junior
- 1 Analista forense digital
- 1 Especialista en comunicaciones de crisis

### 6.3 Comunicación de Incidentes

En caso de brecha de datos, NovaPay notificará:
- A los usuarios afectados dentro de las 72 horas.
- A la CMF según los plazos regulatorios establecidos.
- A la Agencia de Protección de Datos Personales (APDP) conforme a la Ley 21.719.

## 7. Monitoreo y Auditoría

- **SIEM:** Correlación de eventos de seguridad en tiempo real con Splunk Enterprise.
- **SOC 24/7:** Monitoreo continuo por equipo interno y proveedor externo.
- **Pentesting:** Pruebas de penetración trimestrales por empresa externa certificada (CREST).
- **Bug Bounty:** Programa activo con recompensas de $100 USD a $10.000 USD por vulnerabilidad válida.
- **Auditoría interna:** Semestral, evaluando cumplimiento de ISO 27001 y PCI DSS.
- **Auditoría externa:** Anual, realizada por firma Big Four.

## 8. Capacitación y Concientización

- Onboarding de seguridad obligatorio para todos los nuevos colaboradores.
- Simulaciones de phishing mensuales (tasa de click objetivo: menor al 5%).
- Capacitación anual en seguridad de la información (8 horas).
- Módulos especializados para equipos de desarrollo (OWASP, Secure Coding).
- Boletín mensual de ciberseguridad con amenazas actuales y buenas prácticas.

## 9. Continuidad del Negocio

- RPO (Recovery Point Objective): 1 hora para sistemas críticos.
- RTO (Recovery Time Objective): 4 horas para servicios core.
- Centro de datos secundario en modo activo-pasivo con failover automático.
- Ejercicios de recuperación ante desastres (DRP) semestrales.
- Plan de comunicación de crisis documentado y probado.

## 10. Métricas de Seguridad (KPIs)

| Métrica | Objetivo | Frecuencia |
|---------|----------|------------|
| Disponibilidad de la plataforma | ≥ 99.5% | Mensual |
| Tiempo medio de detección (MTTD) | < 30 minutos | Mensual |
| Tiempo medio de respuesta (MTTR) | < 2 horas | Mensual |
| Tasa de falsos positivos en fraudes | < 2% | Semanal |
| Vulnerabilidades críticas sin remediar | 0 (> 30 días) | Semanal |
| Tasa de click en phishing simulado | < 5% | Mensual |
| Cobertura de MFA para colaboradores | 100% | Trimestral |
