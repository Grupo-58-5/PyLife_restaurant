
import pytest
from src.reservations.domain.reservation import Reservation

@pytest.mark.asyncio
async def test_cannot_create_overlapping_reservations(client, get_token_client, insert_restaurant):

    pass
    # # 2. Define los datos de la primera reserva
    # reserv_data_1 = Reservation(
    #     table_id=table.id,
    #     init_time="2025-05-24T19:00:00",
    #     final_time="2025-05-24T20:00:00",
    #     client_id="1"
    # )

    # # 3. Crea la primera reserva exitosamente
    # response_1 = await client.post("/api/v1/reservation/", json=reserv_data_1.dict())
    # assert response_1.status_code == 200
    # reserva_1 = response_1.json()
    # assert reserva_1["table_id"] == table.id

    # # 4. Define los datos de la segunda reserva que se superpone con la primera
    # reserv_data_2 = Reservation(
    #     table_id=table.id,
    #     init_time="2025-05-24T19:30:00",
    #     final_time="2025-05-24T20:30:00",
    #     client_id="1"
    # )

    # # 5. Intenta crear la segunda reserva y verifica que falle
    # response_2 = await client.post("/api/v1/reservation/", json=reserv_data_2.dict())
    # assert response_2.status_code == 409 
    # assert "La mesa no está disponible en este horario" in response_2.json()["detail"] 


def test_cannot_create_reservation_with_invalid_dish(client, get_token_client, insert_restaurant):
    pass
    # # 1. Crea una mesa para las pruebas
    # mesa = Mesa(numero=1)
    # db.add(mesa)
    # db.commit()
    # db.refresh(mesa)

    # # 2. Define los datos de la reserva con un plato inválido
    # reserv_data = Reservation(
    #     mesa_id=mesa.id,
    #     hora_inicio="2025-05-24T19:00:00",
    #     hora_fin="2025-05-24T20:00:00",
    #     client_id="1",
    #     pre_order=["plato_invalido"]
    # )

    # # 3. Intenta crear la reserva y verifica que falle
    # response = client.post("/api/v1/reservation/", json=reserv_data.dict())
    # assert response.status_code == 400
    # assert response.json()["detail"] == f"El plato {reserv_data.plato} no existe en el menú del restaurant"
