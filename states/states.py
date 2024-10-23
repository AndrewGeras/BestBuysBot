from aiogram.fsm.state import StatesGroup, State


class FSMAbstract(StatesGroup):

    """ an abstract class for FSM states"""

    waiting_for_choice: State
    input_item: State
    change_list: State
    delete_item: State


class FSMEditItemsList(StatesGroup):
    waiting_for_choice = State()
    input_item = State()
    change_item = State()
    delete_item = State()
    delete_confirm = State()


class FSMEditStoreList(StatesGroup):
    waiting_for_choice = State()
    input_item = State()
    change_item = State()
    delete_item = State()
    delete_confirm = State()


class FSMEditMatrix(StatesGroup):
    wait_for_store_chs = State()
    wait_for_item_chs = State()
    wait_for_price_input = State()


class FSMShowItems(StatesGroup):
    wait_for_method_chs = State()
    wait_for_store_chs = State()
