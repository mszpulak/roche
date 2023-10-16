import asyncio
from src.schema import Buttons, StatusMessage
from src.logger import server_logger
from transitions import MachineError
from src.errors import HTTPMachineStateError


class ButtonService:
    def __init__(self, state_machine) -> None:
        self.state_machine = state_machine

    async def process_action(self, action: str) -> StatusMessage:
        try:
            match action:
                case Buttons.PLUS_POWER:
                    await self.state_machine.plus_10_power()
                case Buttons.MINUS_POWER:
                    await self.state_machine.minus_10_power()
                case Buttons.PLUS_TIME:
                    await self.state_machine.plus_10_time()
                case Buttons.MINUS_TIME:
                    await self.state_machine.minus_10_time()
                case Buttons.ON:
                    await self.state_machine.enable()
                case Buttons.OFF:
                    await self.state_machine.disable()
                case Buttons.CANCEL:
                    await self.state_machine.cancel()
                case _:
                    server_logger.error("no action taken")
                    await asyncio.sleep(0)
            return self.state_machine.return_status()
        except MachineError as ex:
            server_logger.error(str(ex))
            await asyncio.sleep(0)
            raise HTTPMachineStateError(str(ex))

    async def return_results(self) -> StatusMessage:
        await asyncio.sleep(0)
        return self.state_machine.return_status()
