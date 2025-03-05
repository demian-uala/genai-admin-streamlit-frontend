import streamlit as st
import requests

# URL base del backend
BASE_URL = "https://genai-admin-back-416638675667.us-east4.run.app"

# -------------------------------
# Funciones para interactuar con el backend
# -------------------------------

def get_all_services(skip=0, limit=100):
    """Obtiene el listado de servicios mediante GET /services/all"""
    try:
        response = requests.get(f"{BASE_URL}/services/all", params={"skip": skip, "limit": limit})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al obtener servicios: {e}")
        return None

def create_service(data):
    """Crea un servicio mediante POST /services con el esquema CreateServiceWithRevision"""
    try:
        response = requests.post(f"{BASE_URL}/services", json=data)
        if response.status_code == 201:
            st.success("Servicio creado correctamente")
            return response.json()
        else:
            st.error(f"Error al crear servicio: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_service(service_id):
    """Obtiene un servicio por ID mediante GET /services/{id}"""
    try:
        response = requests.get(f"{BASE_URL}/services/{service_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al obtener servicio: {e}")
        return None

def update_service(service_id, data):
    """Actualiza un servicio mediante PATCH /services/{id} con el esquema UpdateServiceWithRevision"""
    try:
        response = requests.patch(f"{BASE_URL}/services/{service_id}", json=data)
        response.raise_for_status()
        st.success("Servicio actualizado correctamente")
        return response.json()
    except Exception as e:
        st.error(f"Error al actualizar servicio: {e}")
        return None

def delete_service(service_id):
    """Elimina un servicio mediante DELETE /services/{id}"""
    try:
        response = requests.delete(f"{BASE_URL}/services/{service_id}")
        response.raise_for_status()
        st.success("Servicio eliminado correctamente")
        return response.json()
    except Exception as e:
        st.error(f"Error al eliminar servicio: {e}")
        return None

# -------------------------------
# Interfaz de la aplicación
# -------------------------------

st.title("Gestión de Services")

# Menú lateral con las opciones definidas
menu = st.sidebar.radio(
    "Acciones",
    ("Service List", "Create Service", "Get Service", "Update Service", "Delete Service")
)

# -------------------------------
# Página: Listado de Servicios
# -------------------------------
if menu == "Service List":
    st.header("Listado de Servicios")
    skip = st.number_input("Skip", value=0, step=1)
    limit = st.number_input("Limit", value=100, step=1)
    if st.button("Obtener Servicios"):
        services = get_all_services(skip=skip, limit=limit)
        if services:
            st.dataframe(services)

# -------------------------------
# Página: Crear Servicio
# -------------------------------
elif menu == "Create Service":
    st.header("Crear Servicio")
    st.markdown("Ingrese los detalles del servicio:")

    resource_flavor = st.selectbox("Resource Flavor", options=["micro", "standard", "premium", "enterprise"])
    description = st.text_area("Descripción")
    area = st.text_input("Area (ej: platform)")
    project = st.text_input("Project (ej: product)")
    action = st.text_input("Action (ej: testing)")
    available_models = st.multiselect("Available Models", options=["llama", "gemini", "openai"])
    owner = st.text_input("Owner")
    team_input = st.text_input("Team (separar emails con comas)")
    team = [email.strip() for email in team_input.split(",") if email.strip()]

    if st.button("Crear Servicio"):
        if not available_models:
            st.error("Debe seleccionar al menos un modelo disponible.")
        else:
            data = {
                "resource_flavor": resource_flavor,
                "description": description,
                "area": area,
                "project": project,
                "action": action,
                "available_models": available_models,
                "owner": owner,
                "team": team
            }
            create_service(data)

# -------------------------------
# Página: Obtener Servicio por ID
# -------------------------------
elif menu == "Get Service":
    st.header("Obtener Servicio")
    service_id = st.number_input("ID del servicio", min_value=1, step=1)
    if st.button("Obtener Servicio"):
        service = get_service(service_id)
        if service:
            st.json(service)

# -------------------------------
# Página: Actualizar Servicio
# -------------------------------
elif menu == "Update Service":
    st.header("Actualizar Servicio")
    service_id = st.number_input("ID del servicio a actualizar", min_value=1, step=1)
    st.markdown("Ingrese los nuevos valores (opcional):")
    
    new_resource_flavor = st.selectbox("Resource Flavor", options=["", "micro", "standard", "premium", "enterprise"])
    new_description = st.text_area("Nueva Descripción", help="Dejar en blanco si no se actualiza")
    new_action = st.text_input("Nueva Action", help="Dejar en blanco si no se actualiza")
    new_available_models = st.multiselect("Available Models", options=["llama", "gemini", "openai"])
    new_owner = st.text_input("Nuevo Owner", help="Dejar en blanco si no se actualiza")
    new_team_input = st.text_input("Nuevo Team (separar emails con comas)", help="Dejar en blanco si no se actualiza")
    new_team = [email.strip() for email in new_team_input.split(",") if email.strip()] if new_team_input else None

    if st.button("Actualizar Servicio"):
        data = {}
        if new_resource_flavor and new_resource_flavor != "":
            data["resource_flavor"] = new_resource_flavor
        if new_description:
            data["description"] = new_description
        if new_action:
            data["action"] = new_action
        if new_available_models:
            data["available_models"] = new_available_models
        if new_owner:
            data["owner"] = new_owner
        if new_team is not None:
            data["team"] = new_team
        if not data:
            st.error("No se han ingresado datos para actualizar.")
        else:
            update_service(service_id, data)

# -------------------------------
# Página: Eliminar Servicio
# -------------------------------
elif menu == "Delete Service":
    st.header("Eliminar Servicio")
    service_id = st.number_input("ID del servicio a eliminar", min_value=1, step=1)
    if st.button("Eliminar Servicio"):
        delete_service(service_id)
