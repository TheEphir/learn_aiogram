import pkg.weather as weather
import pkg.sale_urls as sales_url
import pkg.sales as sales
import pkg.magnet as k_index

from aiogram import Router, F, html
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup # should use this to add urls into sales things
# from aiogram.utils.keyboard import InlineKeyboardBuilder # this thing can be used if i wanna make slider of sales O_O mb some day

router = Router()

MAIN_KEYBOARD = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Get Current Weather"), ],
    [KeyboardButton(text="Get K-index"), KeyboardButton(text="Get Sales")]
], resize_keyboard=True)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=MAIN_KEYBOARD) # reply markup == keyboard things
    

@router.message(F.text == "Help")
@router.message(Command("help"))
async def get_help(message: Message) -> None:
    """
    Help handler
    """
    await message.answer(f"Help message")
    

@router.message(Command("weather"))
@router.message(F.text == "Get Current Weather")
async def get_current_weather(message: Message) -> None:
    """
    Print weagher info from pkg.weather
    """
    weather_info = weather.get_weahter()
    await message.answer(f"For now\n{weather_info}")
    

@router.message(F.text == "Get Sales")    
@router.message(Command("sales"))    
async def get_current_sales(message: Message) -> None:
    urls = sales_url.read_url_file()
    for key in urls:
        res = sales.get_item_info_rztk(urls[key])
        answ = f"{key}\n{res['price']}"
        await message.answer_photo(
            photo=res["image_url"],
            caption=answ
            )
    

@router.message(F.text == "Get K-index")
@router.message(Command("k_index"))
async def get_k_index(message: Message) -> None:
    index = k_index.get_k_index()
    await message.answer(index)
    
    
# ============= Add item to sale list ==================
class PostSaleItem(StatesGroup):
    name = State()
    item_url = State()
    

@router.message(Command("add_item"))
async def post_sale_item_start(message: Message, state: FSMContext):
    await state.set_state(PostSaleItem.name)
    await message.answer("Enter item")


@router.message(PostSaleItem.name)
async def read_sale_item_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(PostSaleItem.item_url)
    await message.answer("Enter url of item")


@router.message(PostSaleItem.item_url)
async def post_sale_item(message: Message, state: FSMContext):
    await state.update_data(item_url=message.text)
    data = await state.get_data()
    sales.add_item({data["name"]: data["item_url"]})
    answ = f"Item added\n{data['name']}"
    await state.clear()
    await message.answer(answ)
  
    
# =========== Remove item from sale list =========== 
class RemoveSaleItem(StatesGroup):
    name = State()


@router.message(Command("remove_item"))
async def remove_item_from_sale_list_start(message: Message, state: FSMContext):
    await state.set_state(RemoveSaleItem.name)
    keys = sales_url.read_url_file().keys()
    res = f""
    for key in keys:
        res = res +f"\n{key}"
    await message.answer(f"What item u wanna delete?\n{res}")


@router.message(RemoveSaleItem.name)
async def remove_item_from_sale_list_end(message: Message, state: FSMContext):
    item_name = message.text
    sales.remove_item(item_name)
    await state.clear()
    await message.answer(f"Item {item_name} was removed")
    