#!/bin/bash
# =============================================================
# NovaPay AI Agent — Script de Deploy en Oracle Cloud (OCI)
# =============================================================
# Uso: ssh opc@IP_PUBLICA 'bash -s' < deploy/setup_oci.sh
# O copiar a la instancia y ejecutar: chmod +x setup_oci.sh && ./setup_oci.sh
# =============================================================

set -e

echo "============================================"
echo "🏦 NovaPay — Deploy en Oracle Cloud (OCI)"
echo "============================================"

# 1. Actualizar sistema
echo ""
echo "📦 Actualizando sistema..."
sudo dnf update -y

# 2. Instalar Python 3.11 y Git
echo ""
echo "🐍 Instalando Python 3.11 y Git..."
sudo dnf install python3.11 python3.11-pip git -y

# 3. Clonar repositorio
echo ""
echo "📥 Clonando repositorio..."
cd /home/opc
if [ -d "NovaPay-ai-agent" ]; then
    echo "  El directorio ya existe. Actualizando..."
    cd NovaPay-ai-agent
    git pull
else
    # ⚠️ REEMPLAZAR con tu URL de GitHub
    git clone https://github.com/inostroza-Daniela/NovaPay-ai-agent.git
    cd NovaPay-ai-agent
fi

# 4. Instalar dependencias
echo ""
echo "📦 Instalando dependencias de Python..."
pip3.11 install --user -r requirements.txt

# 5. Configurar API Key
echo ""
if [ -z "$GOOGLE_API_KEY" ]; then
    read -p "🔑 Ingresa tu Google API Key: " GOOGLE_API_KEY
    echo "export GOOGLE_API_KEY='$GOOGLE_API_KEY'" >> ~/.bashrc
    export GOOGLE_API_KEY
fi

# 6. Configurar firewall del sistema operativo
echo ""
echo "🔥 Configurando firewall..."
sudo firewall-cmd --permanent --add-port=7860/tcp 2>/dev/null || true
sudo firewall-cmd --reload 2>/dev/null || true

# 7. Crear servicio systemd para ejecución persistente
echo ""
echo "⚙️ Creando servicio systemd..."
sudo tee /etc/systemd/system/novapay-agent.service > /dev/null << EOF
[Unit]
Description=NovaPay AI Agent
After=network.target

[Service]
Type=simple
User=opc
WorkingDirectory=/home/opc/NovaPay-ai-agent
Environment=GOOGLE_API_KEY=$GOOGLE_API_KEY
ExecStart=/usr/bin/python3.11 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 8. Iniciar servicio
echo ""
echo "🚀 Iniciando servicio..."
sudo systemctl daemon-reload
sudo systemctl enable novapay-agent
sudo systemctl start novapay-agent

# 9. Verificar estado
echo ""
echo "============================================"
echo "✅ Deploy completado exitosamente!"
echo "============================================"
echo ""
echo "📌 IMPORTANTE - Configurar Security List en OCI:"
echo "   1. Ve a Networking > Virtual Cloud Networks > tu VCN"
echo "   2. Click en la Subnet > Security Lists > Default"
echo "   3. Agregar Ingress Rule:"
echo "      - Source CIDR: 0.0.0.0/0"
echo "      - IP Protocol: TCP"
echo "      - Destination Port: 7860"
echo ""

# Obtener IP pública
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "NO_DISPONIBLE")
echo "🌐 Tu aplicación estará disponible en:"
echo "   http://${PUBLIC_IP}:7860"
echo ""
echo "📋 Comandos útiles:"
echo "   sudo systemctl status novapay-agent   # Ver estado"
echo "   sudo systemctl restart novapay-agent   # Reiniciar"
echo "   sudo journalctl -u novapay-agent -f    # Ver logs"
echo ""
