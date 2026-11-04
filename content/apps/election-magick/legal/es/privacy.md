# Política de Privacidad

Versión 1.0 · Vigente desde 2026-11-01

Esta Política de Privacidad explica cómo la app Election Magick ("la app") trata la información. La app la ofrece [[OWNER_LEGAL_NAME]], [[OWNER_POSTAL_ADDRESS]] ("nosotros"). Contacto: [[SUPPORT_EMAIL]].

En resumen: la app funciona en tu dispositivo. No operamos servidores, no hay cuentas de usuario y no recibimos tus datos astrológicos, tu ubicación ni las descripciones de tus rituales. Algunas funciones usan servicios de Apple, descritos a continuación.

## 1. Los cálculos se hacen en tu dispositivo

<!-- fact:P-CALC-1 -->
Todos los cálculos astronómicos y astrológicos (posiciones planetarias, casas, horas planetarias, comprobaciones de riesgo, clasificaciones y clasificaciones por rango) se realizan en tu dispositivo. Ningún dato de entrada ni resultado de cálculo se nos envía. No operamos ningún servidor para la app.

## 2. Ubicación

<!-- fact:P-LOC-1 -->
Usar tu ubicación es opcional. La app solo pide permiso después de explicar el motivo, solo "mientras se usa la app" y solo con precisión aproximada (alrededor de 1 km). Siempre puedes elegir una ciudad; todas las funciones funcionan sin acceso a la ubicación.

<!-- fact:P-LOC-2 -->
Si eliges "Usar Ubicación Actual", la app obtiene una posición nueva en cada cálculo. Para encontrar el nombre del lugar y su zona horaria, tus coordenadas se envían al servicio de geocodificación de Apple (Apple Maps). La app no guarda las posiciones obtenidas así, salvo que guardes el lugar.

<!-- fact:P-LOC-3 -->
Al buscar una ciudad, el texto que escribes se envía a Apple Maps para mostrar sugerencias. La ciudad elegida (nombre, país, coordenadas y zona horaria) se guarda en tu dispositivo para que puedas reutilizarla.

El tratamiento de las solicitudes de Maps por parte de Apple se describe en la política de privacidad de Apple: https://www.apple.com/es/legal/privacy/

## 3. Información guardada en tu dispositivo

<!-- fact:P-DATA-1 -->
Las elecciones guardadas, los lugares guardados, las entidades favoritas, los perfiles de ritual y el historial de cálculos se guardan solo en tu dispositivo. Pueden incluir la descripción del ritual que escribiste, la entidad elegida, las coordenadas, el nombre y la zona horaria del lugar y las fechas calculadas.

<!-- fact:P-DATA-2 -->
Tus preferencias (idioma, sistema de casas, nodo lunar, si las explicaciones con IA están activadas) se guardan en tu dispositivo.

<!-- fact:P-DATA-3 -->
Cuando aceptas los Términos de Uso y confirmas haber leído esta Política de Privacidad, la app registra en tu dispositivo qué versiones aceptaste, cuándo y la versión de la app.

## 4. Suscripciones y compras

<!-- fact:P-SUB-1 -->
Las suscripciones las vende, cobra, renueva, cancela y reembolsa Apple a través del App Store. Apple procesa tus datos de pago; nosotros nunca los vemos. La app recibe de Apple solo la información de transacción verificada que necesita para desbloquear tu plan: el producto, las fechas de compra y de vencimiento, los identificadores de la transacción y el estado de renovación.

<!-- fact:P-SUB-2 -->
Cada plan incluye un número de consultas por período. Para contarlas, la app guarda en el Llavero (Keychain) de tu dispositivo (solo en este dispositivo) un registro por período de suscripción formado por resúmenes criptográficos irreversibles (SHA-256) de las consultas ya usadas. Esos resúmenes no contienen el texto de tu ritual, el lugar ni las fechas de forma legible. Este registro se conserva cuando usas "Borrar datos locales", para que la asignación no pueda reiniciarse, y, por el funcionamiento de iOS, puede permanecer en el Llavero después de eliminar la app.

## 5. Explicaciones con IA

<!-- fact:P-AI-1 -->
La IA nunca realiza cálculos astrológicos ni cambia un resultado. Solo redacta explicaciones de resultados que la app ya calculó.

<!-- fact:P-AI-2 -->
Por defecto, las explicaciones las redacta Apple Intelligence en tu dispositivo (modelos Apple Foundation Models). Para ello no se envía nada fuera del dispositivo. Puedes desactivarlas en Ajustes → Explicaciones; la app muestra entonces una explicación estándar generada por ella misma.

<!-- fact:P-AI-3 -->
Private Cloud Compute está desactivado por defecto. Solo se usa si lo activas en Ajustes → Explicaciones → Private Cloud Compute y confirmas la pantalla informativa que se muestra antes de activarlo.

<!-- fact:P-AI-7 -->
Aun activado, Private Cloud Compute se usa solo para textos Premium más largos. Las explicaciones cortas permanecen en tu dispositivo.

<!-- fact:P-AI-4 -->
Cuando se usa Private Cloud Compute, la app envía un resumen compacto de la carta ya calculada: la fecha y la hora locales de la elección con su desfase UTC, la categoría de la intención y el tipo de operación, posiciones y casas del significador y de la Luna, puntuaciones de dignidad, día y hora planetarios, estado de riesgo y riesgos señalados, condición de la Luna, valoración del operador, las razones principales del resultado y la clasificación que tu plan puede mostrar. El identificador de la entidad elegida y su nivel de compatibilidad solo se incluyen cuando el texto solicitado explica esa compatibilidad.

<!-- fact:P-AI-5 -->
Nunca se envían a Private Cloud Compute: coordenadas, nombre del lugar, nombre de la zona horaria, la descripción del ritual que escribiste, notas ni ningún identificador de cuenta o de dispositivo.

<!-- fact:P-AI-6 -->
Apple procesa las solicitudes de Private Cloud Compute en servidores de Apple diseñados para la privacidad; Apple declara que los datos se usan solo para atender la solicitud y no se almacenan ni quedan accesibles para Apple. Consulta https://security.apple.com/blog/private-cloud-compute/ y la política de privacidad de Apple.

<!-- fact:P-AI-8 -->
Tu consentimiento a Private Cloud Compute se registra en tu dispositivo con la versión de la pantalla informativa que confirmaste y la fecha y hora. Desactivar Private Cloud Compute borra ese registro y detiene su uso de inmediato. Si cambiamos la información de forma relevante, la app vuelve a pedir el consentimiento.

<!-- fact:P-AI-9 -->
Ninguna función depende de Private Cloud Compute. Si está desactivado o no disponible (por ejemplo, sin conexión, tras el límite diario de Apple o en dispositivos o regiones no compatibles), las explicaciones provienen de Apple Intelligence en tu dispositivo o de la explicación estándar de la app.

<!-- fact:P-AI-10 -->
La app no usa ningún otro proveedor de IA y no contiene claves de servicios de IA.

## 6. Informes que exportas

<!-- fact:P-EX-1 -->
Los informes (PDF, texto o archivo de datos de Election Magick) se crean en tu dispositivo solo cuando los pides. Solo salen del dispositivo si tú los compartes o guardas mediante la hoja de compartir de iOS; desde ese momento, el servicio que elijas (por ejemplo, correo o una nube) los trata según sus propios términos.

<!-- fact:P-EX-2 -->
Los informes en PDF y texto contienen la elección calculada, el nombre del lugar, su zona horaria y la descripción del ritual que escribiste, pero no las coordenadas del lugar.

<!-- fact:P-EX-3 -->
El archivo de datos de Election Magick (.emreport) contiene además los datos de entrada necesarios para reproducir el cálculo, incluidas las coordenadas del lugar. Compártelo solo con quien quieras que tenga esa información.

<!-- fact:P-EX-4 -->
Las copias temporales creadas para compartir están protegidas por la protección de archivos de iOS y se borran al cabo de una hora.

## 7. Conexiones de red, diagnósticos y publicidad

<!-- fact:P-NET-1 -->
La propia app se conecta solo a servicios de Apple: el App Store (suscripciones), Apple Maps (búsqueda de ciudades y nombres de lugares) y, si lo activas, Private Cloud Compute. Los enlaces que tocas (correo de soporte, nuestro sitio web, el contrato de licencia de Apple, gestión de la suscripción, solicitudes de reembolso) se abren fuera de la app.

<!-- fact:P-DIAG-1 -->
La app no contiene software de analítica, de informes de fallos ni de publicidad. Si activaste "Compartir con desarrolladores" en los Ajustes de iOS, Apple puede compartir con nosotros informes de fallos y estadísticas de uso según describe Apple; puedes desactivarlo en Ajustes → Privacidad y seguridad → Análisis y mejoras.

<!-- fact:P-ADS-1 -->
No mostramos publicidad, no te rastreamos en otras apps o sitios web, no vendemos ni compartimos datos personales y no hay ninguna cuenta que crear.

## 8. Conservación y eliminación de tu información

<!-- fact:P-RET-1 -->
Tu información permanece en tu dispositivo hasta que la borres. No conservamos ninguna copia. Las copias temporales de exportación se borran al cabo de una hora.

<!-- fact:P-DEL-1 -->
Ajustes → Borrar datos locales elimina las elecciones guardadas, los lugares, los favoritos, los perfiles de ritual, el historial, la ubicación elegida, el registro de tu aceptación legal, el estado de la introducción y tu consentimiento a Private Cloud Compute. Los resúmenes de consultas descritos en la sección 4 permanecen. Eliminar la app borra sus datos de tu dispositivo, salvo los elementos que iOS conserva en el Llavero.

Más detalles: Política de Conservación de Datos (en la app, en Ajustes → Legal).

## 9. Menores

<!-- fact:P-KIDS-1 -->
La app no está dirigida a menores ni está diseñada para que la usen menores.

## 10. Tus derechos

<!-- fact:P-RIGHTS-1 -->
Según dónde vivas (por ejemplo, conforme al RGPD de la UE, al UK GDPR o a la LGPD de Brasil), puedes tener derechos de acceso, rectificación, supresión y portabilidad de tus datos personales y de oposición a su uso. Como no conservamos tus datos personales, ejerces estos derechos directamente en la app (ver, exportar o borrar tus datos como se describe arriba). Para cualquier pregunta o reclamación, escribe a [[SUPPORT_EMAIL]]. También puedes reclamar ante una autoridad de protección de datos, como la Agencia Española de Protección de Datos, la autoridad de tu país de la UE/EEE, el Information Commissioner's Office (Reino Unido) o la Autoridad Nacional de Protección de Datos (Brasil).

LEGAL REVIEW REQUIRED: confirmar la identidad del responsable, las bases jurídicas y posibles requisitos de representante en la jurisdicción del titular de la app ([[GOVERNING_LAW]]).

## 11. Cambios

Si cambiamos esta política de forma relevante, la app muestra la nueva versión y te pide que la confirmes antes de continuar. La versión y la fecha de vigencia aparecen al principio.
