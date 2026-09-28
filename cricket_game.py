import random


class CricketGame:
    def __init__(self, overs=2):
        self.overs = overs
        self.balls_per_innings = overs * 6

    def toss(self):
        print("\n=== Toss ===")
        user_call = input("Call heads or tails: ").strip().lower()
        valid = {"heads", "tails"}

        while user_call not in valid:
            print("Please enter either 'heads' or 'tails'.")
            user_call = input("Call heads or tails: ").strip().lower()

        coin = random.choice(["heads", "tails"])
        print(f"The coin shows: {coin}")

        if user_call == coin:
            print("You won the toss!")
            choice = input("Do you want to bat or bowl first? (bat/bowl): ").strip().lower()
            while choice not in {"bat", "bowl"}:
                print("Please choose 'bat' or 'bowl'.")
                choice = input("Do you want to bat or bowl first? (bat/bowl): ").strip().lower()
            return True, choice

        computer_choice = random.choice(["bat", "bowl"])
        print(f"Computer won the toss and chose to {computer_choice} first.")
        return False, computer_choice

    def simulate_ball(self, target=None):
        outcome = random.choices(
            ["W", 0, 1, 2, 3, 4, 6],
            weights=[8, 35, 25, 15, 7, 12, 5],
            k=1,
        )[0]
        return outcome

    def play_innings(self, team_name, target=None, chase=False):
        total = 0
        wickets = 0
        balls = 0

        print(f"\n{team_name} is batting.")
        if target is not None:
            print(f"Target to chase: {target}")

        while balls < self.balls_per_innings and wickets < 10:
            if target is not None and total >= target:
                break

            ball = self.simulate_ball(target)
            balls += 1
            over = (balls - 1) // 6 + 1
            ball_in_over = (balls - 1) % 6 + 1

            if ball == "W":
                wickets += 1
                print(f"Ball {balls}: Wicket! {team_name} - {total}/{wickets}")
            else:
                total += ball
                print(
                    f"Ball {balls}: {ball} run(s) | "
                    f"{team_name} {total}/{wickets} after {over}.{ball_in_over}"
                )

            if target is not None and total >= target:
                print(f"{team_name} reached the target!"
                      )
                break

            if balls >= self.balls_per_innings:
                print(f"Innings over! {team_name} finishes on {total}/{wickets}")
                break

        return {"team": team_name, "runs": total, "wickets": wickets, "balls": balls}

    def display_scorecard(self, innings):
        print(f"\n{innings['team']}: {innings['runs']}/{innings['wickets']} in {innings['balls']} balls")

    def start(self):
        print("Welcome to Cricket Challenge!")
        print("A simple 2-over cricket game in the terminal.")
        user_name = input("Enter your team name: ").strip() or "Your Team"
        computer_name = "CPU XI"

        user_won_toss, toss_choice = self.toss()

        if user_won_toss:
            user_batting_first = toss_choice == "bat"
            computer_batting_first = not user_batting_first
        else:
            user_batting_first = toss_choice == "bowl"
            computer_batting_first = not user_batting_first

        if user_batting_first:
            first_innings = self.play_innings(user_name)
            second_innings = self.play_innings(computer_name, target=first_innings["runs"] + 1, chase=True)
        else:
            first_innings = self.play_innings(computer_name)
            second_innings = self.play_innings(user_name, target=first_innings["runs"] + 1, chase=True)

        self.display_scorecard(first_innings)
        self.display_scorecard(second_innings)

        if user_batting_first:
            if second_innings["runs"] > first_innings["runs"]:
                print(f"\n{computer_name} wins! {second_innings['runs']} vs {first_innings['runs']}")
            elif second_innings["runs"] < first_innings["runs"]:
                print(f"\n{user_name} wins! {first_innings['runs']} vs {second_innings['runs']}")
            else:
                print("\nMatch tied!")
        else:
            if second_innings["runs"] > first_innings["runs"]:
                print(f"\n{user_name} wins! {second_innings['runs']} vs {first_innings['runs']}")
            elif second_innings["runs"] < first_innings["runs"]:
                print(f"\n{computer_name} wins! {first_innings['runs']} vs {second_innings['runs']}")
            else:
                print("\nMatch tied!")

        print("\nThanks for playing Cricket Challenge!")


if __name__ == "__main__":
    game = CricketGame()
    game.start()
