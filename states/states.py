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
    change_list = State()
    delete_item = State()


class FSMEditStoreList(FSMAbstract):
    pass