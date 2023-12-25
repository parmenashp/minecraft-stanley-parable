import time
from src.models import Event


class CooldownManager:
    def __init__(self):
        self.cooldowns = {}
        self.bypass_cooldowns = [Event.PLAYER_DEATH, Event.ADVANCEMENT]

    def add_cooldown(self, name, duration: int):
        self.cooldowns[name] = time.time() + duration

    def is_on_cooldown(self, name) -> bool:
        return time.time() < self.cooldowns.get(name, 0)

    def get_cooldown_remaining(self, name) -> int:
        remaining = self.cooldowns.get(name, 0) - time.time()
        return max(0, remaining)

    def reset_cooldown(self, name):
        self.cooldowns[name] = 0

    def global_cooldown_active(self) -> bool:
        return self.is_on_cooldown("GLOBAL_COOLDOWN")

    def check_all_cooldown(self, event: Event) -> bool:
        """
        Check all cooldowns and return True if any of them is active, False otherwise
        """
        # TODO: if is playing narration return True (hard cd)

        if event in self.bypass_cooldowns:
            print("Bypassing cooldown for event: ", event)
            return False

        if self.global_cooldown_active():
            print("Global cooldown active", self.get_cooldown_remaining("GLOBAL_COOLDOWN"))
            return True

        if self.is_on_cooldown(event):
            print("Cooldown active for event: ", event, self.get_cooldown_remaining(event))
            return True

        return False

    def check_individual_cooldown(self, event: Event) -> bool:
        """
        Check individual cooldown and return True if it is active, False otherwise
        """
        if event in self.bypass_cooldowns:
            print("Bypassing cooldown for event: ", event)
            return False

        if self.is_on_cooldown(event):
            print("Cooldown active for event: ", event, self.get_cooldown_remaining(event))
            return True

        return False
