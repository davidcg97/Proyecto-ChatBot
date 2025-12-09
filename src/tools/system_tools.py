"""
🖥️ System Tools - Diagnóstico del sistema Windows usando PowerShell
"""
from langchain.tools import tool
import subprocess
import platform


@tool
def get_system_performance() -> str:
    """
    Obtiene información de rendimiento del sistema Windows (CPU, RAM).
    Útil cuando el usuario reporta lentitud o problemas de rendimiento.
    
    Returns:
        Información de uso de CPU, RAM y procesos principales
    """
    try:
        result = "🖥️ **Rendimiento del Sistema**\n\n"
        
        # CPU
        cpu_cmd = "Get-WmiObject Win32_Processor | Select-Object -ExpandProperty LoadPercentage"
        cpu_usage = subprocess.check_output(["powershell", "-Command", cpu_cmd], 
                                           text=True, timeout=5).strip()
        result += f"**CPU**: {cpu_usage}% en uso\n"
        
        # RAM
        ram_cmd = """
        $mem = Get-WmiObject Win32_OperatingSystem;
        $total = [math]::Round($mem.TotalVisibleMemorySize/1MB, 2);
        $free = [math]::Round($mem.FreePhysicalMemory/1MB, 2);
        $used = [math]::Round($total - $free, 2);
        $percent = [math]::Round(($used/$total)*100, 2);
        Write-Output "$used GB / $total GB ($percent%)"
        """
        ram_info = subprocess.check_output(["powershell", "-Command", ram_cmd], 
                                          text=True, timeout=5).strip()
        result += f"**RAM**: {ram_info} en uso\n\n"
        
        # Top 5 procesos
        top_cmd = "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, @{Name='CPU';Expression={[math]::Round($_.CPU,2)}}, @{Name='RAM_MB';Expression={[math]::Round($_.WS/1MB,2)}} | Format-Table -AutoSize | Out-String"
        top_processes = subprocess.check_output(["powershell", "-Command", top_cmd], 
                                               text=True, timeout=5).strip()
        result += f"**Top 5 Procesos:**\n```\n{top_processes}\n```\n"
        
        # Recomendaciones
        cpu_val = int(cpu_usage) if cpu_usage.isdigit() else 0
        if cpu_val > 80:
            result += "\n⚠️ **CPU alta**: El sistema está bajo carga. Considera cerrar aplicaciones innecesarias."
        
        return result
        
    except Exception as e:
        return f"❌ Error al obtener información de rendimiento: {str(e)}"


@tool
def check_disk_space() -> str:
    """
    Verifica el espacio disponible en los discos del sistema.
    Útil cuando hay problemas de almacenamiento o el sistema está lento.
    
    Returns:
        Información de espacio usado y disponible en todos los discos
    """
    try:
        disk_cmd = """
        Get-PSDrive -PSProvider FileSystem | 
        Where-Object {$_.Used -ne $null} | 
        Select-Object Name, 
            @{Name='Usado_GB';Expression={[math]::Round($_.Used/1GB,2)}},
            @{Name='Libre_GB';Expression={[math]::Round($_.Free/1GB,2)}},
            @{Name='Total_GB';Expression={[math]::Round(($_.Used+$_.Free)/1GB,2)}},
            @{Name='Porcentaje_Usado';Expression={[math]::Round(($_.Used/($_.Used+$_.Free))*100,2)}} |
        Format-Table -AutoSize | Out-String
        """
        
        disk_info = subprocess.check_output(["powershell", "-Command", disk_cmd], 
                                           text=True, timeout=5).strip()
        
        result = "💾 **Espacio en Discos**\n\n```\n" + disk_info + "\n```\n"
        
        # Advertencia si algún disco está casi lleno
        if "9" in disk_info or "100" in disk_info:
            result += "\n⚠️ **ALERTA**: Algún disco está casi lleno. Considera liberar espacio."
        
        return result
        
    except Exception as e:
        return f"❌ Error al obtener información de discos: {str(e)}"


@tool  
def check_network_connection() -> str:
    """
    Verifica el estado de la conexión de red e internet.
    Útil cuando el usuario reporta problemas de conectividad.
    
    Returns:
        Estado de adaptadores de red y conectividad a internet
    """
    try:
        result = "🌐 **Estado de Red**\n\n"
        
        # Adaptadores activos
        net_cmd = "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object Name, Status, LinkSpeed | Format-Table -AutoSize | Out-String"
        adapters = subprocess.check_output(["powershell", "-Command", net_cmd], 
                                          text=True, timeout=5).strip()
        result += f"**Adaptadores Activos:**\n```\n{adapters}\n```\n"
        
        # Test de internet
        ping_cmd = "Test-Connection -ComputerName 8.8.8.8 -Count 1 -Quiet"
        ping_result = subprocess.check_output(["powershell", "-Command", ping_cmd], 
                                             text=True, timeout=5).strip()
        internet_status = "✅ Conectado" if ping_result == "True" else "❌ Sin conexión"
        result += f"\n**Internet**: {internet_status}\n"
        
        if ping_result != "True":
            result += "\n⚠️ **Sin conexión a internet**. Verifica:\n"
            result += "   - Cable de red conectado\n"
            result += "   - WiFi activado\n"
            result += "   - Configuración de proxy\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error al verificar la red: {str(e)}"
