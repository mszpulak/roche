from transitions.extensions.asyncio import AsyncMachine
from src.schema import MicrowaveState, StatusMessage
from src.redis_session import Cacher, get_redis_client


class MicrowaveMachine:
    transitions = [
        ["enable", MicrowaveState.off, MicrowaveState.on],
        ["disable", MicrowaveState.on, MicrowaveState.off],
        dict(
            trigger="plus_10_power",
            source=MicrowaveState.on,
            dest=None,
            after="after_plus_10_power",
        ),
        dict(
            trigger="minus_10_power",
            source=MicrowaveState.on,
            dest=None,
            after="after_minus_10_power",
        ),
        dict(
            trigger="plus_10_time",
            source=MicrowaveState.on,
            dest=None,
            after="after_plus_10_time",
        ),
        dict(
            trigger="minus_10_time",
            source=MicrowaveState.on,
            dest=None,
            after="after_minus_10_time",
        ),
        dict(
            trigger="cancel",
            source=MicrowaveState.on,
            dest=MicrowaveState.off,
            after="after_cancel",
        ),
    ]

    """ transition signature:
    source, dest, conditions = None, unless = None, before = None,
    after = None, prepare = None
    """

    def __init__(self) -> None:
        self.machine = AsyncMachine(
            model=self,
            states=MicrowaveState,
            transitions=self.transitions,
            initial=MicrowaveState.off,
        )
        self.initial_power: int = 600
        self.initial_time: int = 60
        self.current_power: int = self.initial_power
        self.current_time: int = self.initial_time

    def return_status(self) -> StatusMessage:
        return StatusMessage(
            power=self.current_power,
            time=self.current_time,
            state=self.state,
        )

    async def on_enter_on(self) -> None:
        print("on_enter_on")

    async def on_enter_off(self) -> None:
        print("on_enter_off")

    async def after_plus_10_power(self) -> None:
        if self.current_power > 0:
            self.current_power += 0.1 * self.initial_power

    async def after_minus_10_power(self) -> None:
        if self.current_power > 0:
            self.current_power -= 0.1 * self.initial_power

    async def after_plus_10_time(self) -> None:
        if self.current_time > 0:
            self.current_time += 10

    async def after_minus_10_time(self) -> None:
        if self.current_time > 0:
            self.current_time -= 10

    async def after_cancel(self) -> None:
        self.current_power = self.initial_power
        self.current_time = self.initial_time


@Cacher(next(get_redis_client()))
def create_state_machine():
    return MicrowaveMachine()


state_machine = create_state_machine()
