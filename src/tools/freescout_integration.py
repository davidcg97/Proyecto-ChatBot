import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, Optional

load_dotenv()

class FreeScoutDB:
    """Integración directa con la base de datos de FreeScout."""
    
    def __init__(self):
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'freescout'),
            'password': os.getenv('MYSQL_PASSWORD', 'freescout_password'),
            'database': os.getenv('MYSQL_DATABASE', 'freescout')
        }
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return mysql.connector.connect(**self.config)
    
    def create_ticket(self, subject: str, body: str, 
                     customer_email: str = "usuario@empresa.local",
                     priority: int = 2) -> Dict:
        """
        Crea un ticket directamente en la base de datos de FreeScout.
        
        Args:
            subject: Asunto del ticket
            body: Descripción del problema
            customer_email: Email del usuario que reporta
            priority: Prioridad (no se usa directamente en esta versión)
        
        Returns:
            Dict con la información del ticket creado
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # 1. Obtener el mailbox_id y folder_id (inbox)
            cursor.execute("SELECT id FROM mailboxes ORDER BY id LIMIT 1")
            result = cursor.fetchone()
            if not result:
                raise Exception("No hay mailboxes configurados en FreeScout")
            mailbox_id = result[0]
            
            # 2. Obtener el folder_id del inbox (type=1 es inbox)
            cursor.execute("""
                SELECT id FROM folders 
                WHERE mailbox_id = %s AND type = 1 
                LIMIT 1
            """, (mailbox_id,))
            folder_result = cursor.fetchone()
            folder_id = folder_result[0] if folder_result else 1
            
            # 3. Obtener el siguiente número de conversación
            cursor.execute("""
                SELECT COALESCE(MAX(number), 0) + 1 FROM conversations 
                WHERE mailbox_id = %s
            """, (mailbox_id,))
            conversation_number = cursor.fetchone()[0]
            
            # 4. Buscar o crear customer (opcional, puede ser NULL)
            cursor.execute("""
                SELECT id FROM customers 
                WHERE LOWER(first_name) = LOWER(%s) 
                LIMIT 1
            """, ("Usuario IT",))
            
            customer = cursor.fetchone()
            if customer:
                customer_id = customer[0]
            else:
                cursor.execute("""
                    INSERT INTO customers (first_name, last_name, created_at, updated_at)
                    VALUES (%s, %s, NOW(), NOW())
                """, ("Usuario", "IT"))
                customer_id = cursor.lastrowid
            
            # 5. Crear la conversación (ticket)
            cursor.execute("""
                INSERT INTO conversations 
                (number, type, folder_id, status, state, subject, 
                 customer_email, preview, mailbox_id, customer_id,
                 source_via, source_type, last_reply_at, last_reply_from,
                 created_at, updated_at)
                VALUES (%s, 1, %s, 1, 2, %s, %s, %s, %s, %s, 1, 8, NOW(), 2, NOW(), NOW())
            """, (conversation_number, folder_id, subject, customer_email, 
                  body[:100], mailbox_id, customer_id))
            
            conversation_id = cursor.lastrowid
            
            # 6. Crear el primer thread (mensaje del ticket)
            cursor.execute("""
                INSERT INTO threads 
                (conversation_id, type, status, state, body, 
                 `from`, customer_id, source_via, source_type,
                 first, created_at, updated_at)
                VALUES (%s, 1, 1, 2, %s, %s, %s, 1, 8, 1, NOW(), NOW())
            """, (conversation_id, body, customer_email, customer_id))
            
            # 7. Actualizar el contador de threads en la conversación
            cursor.execute("""
                UPDATE conversations 
                SET threads_count = 1
                WHERE id = %s
            """, (conversation_id,))
            
            conn.commit()
            
            return {
                "success": True,
                "ticket_id": conversation_id,
                "number": conversation_number,
                "subject": subject,
                "customer_email": customer_email,
                "created_at": datetime.now().isoformat(),
                "message": f"✅ Ticket #{conversation_number} creado correctamente"
            }
            
        except Exception as e:
            conn.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Error al crear ticket: {str(e)}"
            }
        finally:
            cursor.close()
            conn.close()
    
    def get_ticket(self, ticket_id: int) -> Optional[Dict]:
        """Consulta la información de un ticket por su ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT c.id, c.number, c.subject, c.status, c.customer_email,
                       c.created_at, c.updated_at, t.body
                FROM conversations c
                LEFT JOIN threads t ON t.conversation_id = c.id AND t.first = 1
                WHERE c.id = %s
                LIMIT 1
            """, (ticket_id,))
            
            row = cursor.fetchone()
            
            if row:
                status_map = {1: "Activo", 2: "Pendiente", 3: "Cerrado"}
                return {
                    "ticket_id": row[0],
                    "number": row[1],
                    "subject": row[2],
                    "status": status_map.get(row[3], "Desconocido"),
                    "customer_email": row[4],
                    "created_at": row[5],
                    "updated_at": row[6],
                    "description": row[7] if row[7] else "Sin descripción"
                }
            return None
            
        finally:
            cursor.close()
            conn.close()
    
    def get_ticket_by_number(self, ticket_number: int) -> Optional[Dict]:
        """Consulta la información de un ticket por su número visible"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT c.id, c.number, c.subject, c.status, c.customer_email,
                       c.created_at, c.updated_at, t.body
                FROM conversations c
                LEFT JOIN threads t ON t.conversation_id = c.id AND t.first = 1
                WHERE c.number = %s
                LIMIT 1
            """, (ticket_number,))
            
            row = cursor.fetchone()
            
            if row:
                status_map = {1: "Activo", 2: "Pendiente", 3: "Cerrado"}
                return {
                    "ticket_id": row[0],
                    "number": row[1],
                    "subject": row[2],
                    "status": status_map.get(row[3], "Desconocido"),
                    "customer_email": row[4],
                    "created_at": row[5],
                    "updated_at": row[6],
                    "description": row[7] if row[7] else "Sin descripción"
                }
            return None
            
        finally:
            cursor.close()
            conn.close()

# Instancia global
_freescout_db = None

def get_freescout_db():
    """Retorna una instancia singleton de FreeScoutDB"""
    global _freescout_db
    if _freescout_db is None:
        _freescout_db = FreeScoutDB()
    return _freescout_db