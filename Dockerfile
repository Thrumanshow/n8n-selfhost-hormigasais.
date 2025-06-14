# Usamos la imagen oficial de n8n
FROM n8nio/n8n:latest

# Variables de entorno para autenticación
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=hormigasais123

# Puerto por defecto que expone n8n
EXPOSE 5678

# Comando para iniciar n8n
CMD ["n8n"]
