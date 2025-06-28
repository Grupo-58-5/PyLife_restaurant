


from uuid import uuid4
from src.restaurants.application.schemas.entry.resaurant_schema_entry import CreateRestaurantSchema
from src.restaurants.application.schemas.response.menu_item_response import MenuItemBase
from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse, RestaurantDetailResponse
from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.domain.vo.restaurant_address import RestaurantAddress
from src.restaurants.domain.vo.restaurant_name import RestaurantName
from src.restaurants.domain.vo.restaurant_schedule import RestaurantSchedule
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class CreateRestaurantApplicationService(IApplicationService[CreateRestaurantSchema, Result[RestaurantDetailResponse]]):
    def __init__(self, restaurant_repository: IRestaurantRepository):
        self.repository = restaurant_repository

    async def execute(self, data: CreateRestaurantSchema) -> Result[RestaurantDetailResponse]:
        try:
            restaurant_id = uuid4()

            # #? Validate that the restaurant does not already exist
            # existing_restaurants = await self.repository.get_restaurant_by_name(data.name)
            # if existing_restaurants:
            #     raise ValueError(f"Restaurant with name '{data.name}' already exists.")

            restaurant = Restaurant.create(
                id=restaurant_id,
                name=RestaurantName.create(data.name),
                address=RestaurantAddress.create(data.address),
                schedule=RestaurantSchedule.create(opening_time=data.opening_hour, closing_time=data.closing_hour),
            )
            # print(f"Creating restaurant with ID: {restaurant_id}")
            # print("Everything is ok, creating restaurant...")
            # print(restaurant.get_opening())

            #? Add menu items if provided
            if data.menu_items:
                for item in data.menu_items:
                    menu_item = MenuEntity.create(
                        id= uuid4(),
                        name=item.name,
                        description=item.description,
                        category=item.category
                    )
                    restaurant.add_menu_item(menu_item)
            else:
                print("No menu items provided, creating restaurant without menu.")

            saved_restaurant = await self.repository.create_restaurant(restaurant)
            if not saved_restaurant.is_succes():
                return Result.failure(Exception('Strange error saving restaurant'), saved_restaurant.messg, 400)

            restaurant = saved_restaurant.result()
            # print(restaurant)
            return Result.success(
                RestaurantDetailResponse(
                    id=restaurant.get_id(),
                    name=restaurant.get_name(),
                    address=restaurant.get_address(),
                    opening_hour=restaurant.get_opening(),
                    closing_hour=restaurant.get_closing(),
                    menu= [
                        MenuItemBase(
                            id=item.id,
                            name=item.get_name(),
                            description=item.get_description(),
                            category=item.get_category()
                        ) for item in restaurant.get_menu()
                    ],
                    tables=[]  # Assuming no tables are defined at creation, can be added later
                ))
        except ValueError as ve:
            print('veee')
            return Result.failure(Exception(str(ve)), str(ve), 400)
        except Exception as e:
            return Result.failure(e, str(e))
