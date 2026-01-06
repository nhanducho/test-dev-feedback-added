from otree.api import *
import random


doc = """
Supply Chain Resilience Spending Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'test_without_quiz_rounding_10'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 100
    INITIAL_PROFIT = 10000
    GROSS_PROFIT = 100
    DISRUPTION_COST = 2000
    BASIC_PROBABILITY = 5
    SHOW_UP_FEE = 3.0
    CONVERSION_RATE = 1 / 1500


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Spending Game fields
    money_input = models.IntegerField(min=0, max=100, label="", blank=False)
    is_disrupted = models.BooleanField(initial=False)
    cost_of_disruption = models.IntegerField(initial=0)
    accumulative_total_costs = models.IntegerField(initial=0)
    round_total_costs = models.FloatField(initial=0)
    round_profit = models.FloatField(initial=0)
    expected_profit = models.IntegerField(initial=C.INITIAL_PROFIT)
    round_calculated = models.BooleanField(initial=False)

    # Time tracking fields for each page
    welcoming_page_loaded = models.StringField(initial='')
    welcoming_form_submitted = models.StringField(initial='')
    instruction1_page_loaded = models.StringField(initial='')
    instruction1_form_submitted = models.StringField(initial='')
    instruction2_page_loaded = models.StringField(initial='')
    instruction2_form_submitted = models.StringField(initial='')
    payment_page_loaded = models.StringField(initial='')
    payment_form_submitted = models.StringField(initial='')
    question_page_loaded = models.StringField(initial='')
    question_form_submitted = models.StringField(initial='')
    game_page_loaded = models.StringField(initial='')
    game_form_submitted = models.StringField(initial='')
    game_result_page_loaded = models.StringField(initial='')
    game_result_form_submitted = models.StringField(initial='')
    extra_task1_page_loaded = models.StringField(initial='')
    extra_task1_form_submitted = models.StringField(initial='')
    extra_task2_page_loaded = models.StringField(initial='')
    extra_task2_form_submitted = models.StringField(initial='')
    extra_task_result_page_loaded = models.StringField(initial='')
    extra_task_result_form_submitted = models.StringField(initial='')
    demographic_page_loaded = models.LongStringField(initial='')
    demographic_form_submitted = models.LongStringField(initial='')

    # Duration fields in seconds for each page
    welcoming_duration = models.FloatField(initial=0)
    instruction1_duration = models.FloatField(initial=0)
    instruction2_duration = models.FloatField(initial=0)
    payment_duration = models.FloatField(initial=0)
    question_duration = models.FloatField(initial=0)
    game_duration = models.FloatField(initial=0)
    game_result_duration = models.FloatField(initial=0)
    extra_task1_duration = models.FloatField(initial=0)
    extra_task2_duration = models.FloatField(initial=0)
    extra_task_result_duration = models.FloatField(initial=0)
    demographic_duration = models.FloatField(initial=0)
    total_duration = models.FloatField(initial=0)
    total_duration_excluding_results = models.FloatField(initial=0)


class CombinedResult(ExtraModel):
    player = models.Link(Player)
    spending = models.IntegerField()
    is_disrupted = models.BooleanField()
    cost_of_disruption = models.IntegerField()
    round_total_costs = models.FloatField(initial=0)
    round_profit = models.FloatField(initial=0)
    accumulative_total_costs = models.IntegerField(initial=0)
    expected_profit = models.IntegerField(initial=C.INITIAL_PROFIT)


# PAGES
class WelcomingPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def live_method(player, data):
        if "page_loaded" in data:
            prev = player.field_maybe_none('welcoming_page_loaded') or ''
            player.welcoming_page_loaded = prev + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            prev = player.field_maybe_none('welcoming_form_submitted') or ''
            player.welcoming_form_submitted = prev + str(data['form_submitted']) + ", "


class InstructionPage1(Page):
    allow_back_button = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def live_method(player, data):
        if "page_loaded" in data:
            prev = player.field_maybe_none('instruction1_page_loaded') or ''
            player.instruction1_page_loaded = prev + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            prev = player.field_maybe_none('instruction1_form_submitted') or ''
            player.instruction1_form_submitted = prev + str(data['form_submitted']) + ", "


class InstructionPage2(Page):
    allow_back_button = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def live_method(player, data):
        if "page_loaded" in data:
            prev = player.field_maybe_none('instruction2_page_loaded') or ''
            player.instruction2_page_loaded = prev + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            prev = player.field_maybe_none('instruction2_form_submitted') or ''
            player.instruction2_form_submitted = prev + str(data['form_submitted']) + ", "


class PaymentInfo(Page):
    allow_back_button = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def live_method(player, data):
        if "page_loaded" in data:
            prev = player.field_maybe_none('payment_page_loaded') or ''
            player.payment_page_loaded = prev + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            prev = player.field_maybe_none('payment_form_submitted') or ''
            player.payment_form_submitted = prev + str(data['form_submitted']) + ", "


class GamePage(Page):
    form_model = 'player'
    form_fields = ['money_input']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 0

    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        results = []
        for p in all_players[:player.round_number]:
            player_results = CombinedResult.filter(player=p)
            for r in player_results:
                r.round_total_costs = r.spending + r.cost_of_disruption
                r.round_profit = 100 - r.spending - r.cost_of_disruption
            results.extend(player_results)

        results = sorted(results, key=lambda x: x.player.round_number, reverse=True)

        current_round_result = None
        if player.round_calculated:
            current_results = CombinedResult.filter(player=player)
            if current_results:
                current_round_result = current_results[0]

        last_result = results[0] if results else None

        accumulative_costs = 0
        if results:
            accumulative_costs = sum(r.spending + r.cost_of_disruption for r in results)

        accumulative_profit = 0
        if results:
            accumulative_profit = sum(100 - r.spending - r.cost_of_disruption for r in results)

        current_profit = last_result.expected_profit if last_result else C.INITIAL_PROFIT

        game_completed = (player.round_number == C.NUM_ROUNDS and
                          len(CombinedResult.filter(player=player)) > 0)

        final_stats = None
        if game_completed:
            total_spending = sum(r.spending for r in results)
            total_disruption_cost = sum(r.cost_of_disruption for r in results)
            final_profit = results[0].expected_profit if results else C.INITIAL_PROFIT

            final_stats = {
                'total_spending': total_spending,
                'total_disruption_cost': total_disruption_cost,
                'final_profit': final_profit,
                'initial_profit': C.INITIAL_PROFIT,
                'all_results': results,
            }

        return dict(
            combined_result=results,
            current_round_result=current_round_result,
            last_result=last_result,
            accumulative_costs=accumulative_costs,
            accumulative_profit=accumulative_profit,
            initial_profit=C.INITIAL_PROFIT,
            current_profit=current_profit,
            is_final_round=player.round_number == C.NUM_ROUNDS,
            game_completed=game_completed,
            final_stats=final_stats,
            round_calculated=player.round_calculated,
        )

    @staticmethod
    def live_method(player: Player, data):
        if "page_loaded" in data:
            player.game_page_loaded = player.field_maybe_none('game_page_loaded') + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            player.game_form_submitted = player.field_maybe_none('game_form_submitted') + str(
                data['form_submitted']) + ", "
        if 'action' in data and data['action'] == 'calculate_result':
            spending = data['spending']

            if spending < 0 or spending > 100:
                return {'status': 'error', 'message': 'spending must be between 0 and 100'}

            player.money_input = spending

            disruption_probability = C.BASIC_PROBABILITY * (1 - spending / 100)
            disruption_probability = max(0, disruption_probability)

            disruption_impact = C.DISRUPTION_COST * (1 - spending / 100)
            disruption_impact = max(0, int(disruption_impact))

            random_number = random.uniform(0, 100)

            if random_number < disruption_probability:
                player.is_disrupted = True
                player.cost_of_disruption = disruption_impact
            else:
                player.is_disrupted = False
                player.cost_of_disruption = 0

            if player.round_number > 1:
                prev_player = player.in_round(player.round_number - 1)
                prev_results = CombinedResult.filter(player=prev_player)
                if prev_results:
                    prev_expected_profit = prev_results[0].expected_profit
                    prev_accumulative_total_costs = prev_results[0].accumulative_total_costs
                else:
                    prev_expected_profit = C.INITIAL_PROFIT
                    prev_accumulative_total_costs = 0

                player.expected_profit = prev_expected_profit - spending - player.cost_of_disruption
                player.accumulative_total_costs = prev_accumulative_total_costs + spending + player.cost_of_disruption
            else:
                player.expected_profit = C.INITIAL_PROFIT - spending - player.cost_of_disruption
                player.accumulative_total_costs = spending + player.cost_of_disruption

            existing_results = CombinedResult.filter(player=player)
            for result in existing_results:
                result.delete()

            CombinedResult.create(
                player=player,
                spending=spending,
                is_disrupted=player.is_disrupted,
                cost_of_disruption=player.cost_of_disruption,
                round_total_costs=player.round_total_costs,
                round_profit=player.round_profit,
                accumulative_total_costs=player.accumulative_total_costs,
                expected_profit=player.expected_profit,
            )

            player.round_calculated = True

            return {
                'status': 'success',
                'result': {
                    'round': player.round_number,
                    'spending': spending,
                    'is_disrupted': player.is_disrupted,
                    'disruption_probability': round(disruption_probability, 2),
                    'disruption_impact_if_occurs': disruption_impact,
                    'cost_of_disruption': player.cost_of_disruption,
                    'accumulative_total_costs': player.accumulative_total_costs,
                    'expected_profit': player.expected_profit,
                }
            }

        elif data['action'] == 'next_round':
            player.round_calculated = False
            return {'status': 'next_round'}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not player.round_calculated and player.money_input is not None:
            spending = player.money_input

            disruption_probability = C.BASIC_PROBABILITY * (1 - spending / 100)
            disruption_probability = max(0, disruption_probability)

            disruption_impact = C.DISRUPTION_COST * (1 - spending / 100)
            disruption_impact = max(0, int(disruption_impact))

            random_number = random.uniform(0, 100)

            if random_number < disruption_probability:
                player.is_disrupted = True
                player.cost_of_disruption = disruption_impact
            else:
                player.is_disrupted = False
                player.cost_of_disruption = 0

            if player.round_number > 1:
                prev_player = player.in_round(player.round_number - 1)
                prev_results = CombinedResult.filter(player=prev_player)
                if prev_results:
                    prev_expected_profit = prev_results[0].expected_profit
                    prev_accumulative_total_costs = prev_results[0].accumulative_total_costs
                else:
                    prev_expected_profit = C.INITIAL_PROFIT
                    prev_accumulative_total_costs = 0

                player.expected_profit = prev_expected_profit - spending - player.cost_of_disruption
                player.accumulative_total_costs = prev_accumulative_total_costs + spending + player.cost_of_disruption
            else:
                player.expected_profit = C.INITIAL_PROFIT - spending - player.cost_of_disruption
                player.accumulative_total_costs = spending + player.cost_of_disruption

            existing_results = CombinedResult.filter(player=player)
            for result in existing_results:
                result.delete()

            CombinedResult.create(
                player=player,
                spending=spending,
                is_disrupted=player.is_disrupted,
                cost_of_disruption=player.cost_of_disruption,
                round_total_costs=player.round_total_costs,
                round_profit=player.round_profit,
                accumulative_total_costs=player.accumulative_total_costs,
                expected_profit=player.expected_profit,
            )


class GameResultPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        all_results = []
        for p in all_players:
            player_results = CombinedResult.filter(player=p)
            all_results.extend(player_results)

        all_results = sorted(all_results, key=lambda x: x.player.round_number)

        total_spending = sum(r.spending for r in all_results)
        total_disruption_cost = sum(r.cost_of_disruption for r in all_results)
        final_profit = all_results[-1].expected_profit if all_results else C.INITIAL_PROFIT
        average_spending = total_spending // C.NUM_ROUNDS if all_results else 0
        num_disruptions = sum(1 for r in all_results if r.is_disrupted)

        # Calculate the payoff relative to performance
        performance_payment = round(float(final_profit) * C.CONVERSION_RATE, 1)

        # Calculate the total game payment
        total_payment = round(C.SHOW_UP_FEE + performance_payment, 1)

        player.participant.payoff = performance_payment

        return dict(
            all_results=all_results,
            total_results=len(all_results),
            num_disruptions=num_disruptions,
            total_disruption_cost=total_disruption_cost,
            total_spending=total_spending,
            final_profit=final_profit,
            initial_profit=C.INITIAL_PROFIT,
            average_spending=average_spending,
            show_up_fee=C.SHOW_UP_FEE,
            performance_payment=performance_payment,
            total_payment=total_payment,
        )

    @staticmethod
    def live_method(player, data):
        if "page_loaded" in data:
            prev = player.field_maybe_none('game_result_page_loaded') or ''
            player.game_result_page_loaded = prev + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            prev = player.field_maybe_none('game_result_form_submitted') or ''
            player.game_result_form_submitted = prev + str(data['form_submitted']) + ", "


class ExtraTask1(Page):
    form_model = 'player'
    form_fields = ['task1_d1', 'task1_d2', 'task1_d3', 'task1_d4', 'task1_d5',
                   'task1_d6', 'task1_d7', 'task1_d8', 'task1_d9', 'task1_d10']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.task1_selected_decision = random.randint(1, 10)
        player.task1_random_number = random.randint(1, 10)

        decision_field = f'task1_d{player.task1_selected_decision}'
        choice = getattr(player, decision_field)

        decisions = {
            1: {'A': {'other': 750}, 'B': {1: 1750, 'other': 0}},
            2: {'A': {'other': 750}, 'B': {1: 1750, 2: 1750, 'other': 0}},
            3: {'A': {'other': 750}, 'B': {1: 1750, 2: 1750, 3: 1750, 'other': 0}},
            4: {'A': {'other': 750}, 'B': {1: 1750, 2: 1750, 3: 1750, 4: 1750, 'other': 0}},
            5: {'A': {'other': 750}, 'B': {1: 1750, 2: 1750, 3: 1750, 4: 1750, 5: 1750, 'other': 0}},
            6: {'A': {'other': 750}, 'B': {1: 1750, 2: 1750, 3: 1750, 4: 1750, 5: 1750, 6: 1750, 'other': 0}},
            7: {'A': {'other': 750}, 'B': {1: 1750, 2: 1750, 3: 1750, 4: 1750, 5: 1750, 6: 1750, 7: 1750, 'other': 0}},
            8: {'A': {'other': 750},
                'B': {1: 1750, 2: 1750, 3: 1750, 4: 1750, 5: 1750, 6: 1750, 7: 1750, 8: 1750, 'other': 0}},
            9: {'A': {'other': 750},
                'B': {1: 1750, 2: 1750, 3: 1750, 4: 1750, 5: 1750, 6: 1750, 7: 1750, 8: 1750, 9: 1750, 'other': 0}},
            10: {'A': {'other': 750},
                 'B': {1: 1750, 2: 1750, 3: 1750, 4: 1750, 5: 1750, 6: 1750, 7: 1750, 8: 1750, 9: 1750, 10: 1750,
                       'other': 0}},
        }

        decision_payoffs = decisions[player.task1_selected_decision][choice]
        if player.task1_random_number in decision_payoffs:
            player.task1_payoff = decision_payoffs[player.task1_random_number]
        else:
            player.task1_payoff = decision_payoffs['other']

    @staticmethod
    def live_method(player, data):
        if "page_loaded" in data:
            prev = player.field_maybe_none('extra_task1_page_loaded') or ''
            player.extra_task1_page_loaded = prev + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            prev = player.field_maybe_none('extra_task1_form_submitted') or ''
            player.extra_task1_form_submitted = prev + str(data['form_submitted']) + ", "

class ExtraTask2 (Page):
    form_model = 'player'
    form_fields = ['task2_g1', 'task2_g2', 'task2_g3', 'task2_g4', 'task2_g5', 'task2_g6']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.task2_selected_gamble = random.randint(1, 6)

        gamble_field = f'task2_g{player.task2_selected_gamble}'
        choice = getattr(player, gamble_field)

        gambles = {
            1: (-200, 600),
            2: (-300, 600),
            3: (-400, 600),
            4: (-500, 600),
            5: (-600, 600),
            6: (-700, 600),
        }

        if choice == 'Reject':
            player.task2_payoff = 0
            player.task2_outcome = 0
        else:
            outcome = random.choice([0, 1])
            player.task2_outcome = outcome

            if outcome == 0:
                player.task2_payoff = gambles[player.task2_selected_gamble][0]
            else:
                player.task2_payoff = gambles[player.task2_selected_gamble][1]

    @staticmethod
    def live_method(player, data):
        if "page_loaded" in data:
            prev = player.field_maybe_none('extra_task2_page_loaded') or ''
            player.extra_task2_page_loaded = prev + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            prev = player.field_maybe_none('extra_task2_form_submitted') or ''
            player.extra_task2_form_submitted = prev + str(data['form_submitted']) + ", "


class ExtraTaskResult(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        all_results = []
        for p in all_players:
            player_results = CombinedResult.filter(player=p)
            all_results.extend(player_results)

        all_results = sorted(all_results, key=lambda x: x.player.round_number)

        total_spending = sum(r.spending for r in all_results)
        total_disruption_cost = sum(r.cost_of_disruption for r in all_results)
        final_profit = all_results[-1].expected_profit if all_results else C.INITIAL_PROFIT

        performance_payment = float(final_profit) * C.CONVERSION_RATE
        performance_payment = round(performance_payment, 1)
        spending_game_payment = C.SHOW_UP_FEE + performance_payment

        # Calculate tasks payment (convert ECU to Euro)
        task1_payment = round(player.task1_payoff * C.CONVERSION_RATE, 1)
        task2_payment = round(player.task2_payoff * C.CONVERSION_RATE, 1)
        tasks_total_payment = round(task1_payment + task2_payment, 1)

        # Total payment
        total_payment = round(spending_game_payment + tasks_total_payment, 1)
        player.participant.payoff = tasks_total_payment + performance_payment

        return dict(
            # Spending game
            final_profit=final_profit,
            initial_profit=C.INITIAL_PROFIT,
            show_up_fee=C.SHOW_UP_FEE,
            performance_payment=performance_payment,
            spending_game_payment=spending_game_payment,

            # Extra task 1
            task1_selected_decision=player.task1_selected_decision,
            task1_random_number=player.task1_random_number,
            task1_choice=getattr(player, f'task1_d{player.task1_selected_decision}'),
            task1_payoff=player.task1_payoff,
            task1_payment=task1_payment,

            # Task 2
            task2_selected_gamble=player.task2_selected_gamble,
            task2_choice=getattr(player, f'task2_g{player.task2_selected_gamble}'),
            task2_outcome=player.task2_outcome,
            task2_payoff=player.task2_payoff,
            task2_payment=task2_payment,

            # Totals
            tasks_total_payment=tasks_total_payment,
            total_payment=total_payment,
        )

    @staticmethod
    def live_method(player, data):
        if "page_loaded" in data:
            prev = player.field_maybe_none('extra_task_result_page_loaded') or ''
            player.extra_task_result_page_loaded = prev + str(data['page_loaded']) + ", "
        if "form_submitted" in data:
            prev = player.field_maybe_none('extra_task_result_form_submitted') or ''
            player.extra_task_result_form_submitted = prev + str(data['form_submitted']) + ", "


class EndingPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        all_results = []
        for p in all_players:
            player_results = CombinedResult.filter(player=p)
            all_results.extend(player_results)

        all_results = sorted(all_results, key=lambda x: x.player.round_number)

        total_spending = sum(r.spending for r in all_results)
        total_disruption_cost = sum(r.cost_of_disruption for r in all_results)
        final_profit = all_results[-1].expected_profit if all_results else C.INITIAL_PROFIT

        # Calculate game payments
        performance_payment = float(final_profit) * C.CONVERSION_RATE
        performance_payment = round(performance_payment, 1)
        if performance_payment <= 0: performance_payment = 0
        spending_game_payment = C.SHOW_UP_FEE + performance_payment

        # Calculate tasks payment
        task1_payment = round(player.task1_payoff * C.CONVERSION_RATE, 1)
        task2_payment = round(player.task2_payoff * C.CONVERSION_RATE, 1)
        tasks_total_payment = round(task1_payment + task2_payment, 1)

        # Total payment
        total_payment = round(spending_game_payment + tasks_total_payment, 1)

def custom_export_game(players):
    players = sorted(players, key=lambda p: (p.id_in_group, p.round_number))

    yield [
        'player_id',
        'player_code',
        'round_number',
        'spending',
        'is_disrupted',
        'cost_of_disruption',
        'round_total_costs',
        'round_profit',
        'accumulative_total_costs',
        'expected_profit',
    ]

    for p in players:
        results = CombinedResult.filter(player=p)
        for r in results:
            yield [
                p.id_in_group,
                p.participant.code,
                p.round_number,
                r.spending,
                1 if r.is_disrupted else 0,
                r.cost_of_disruption,
                r.round_total_costs,
                r.round_profit,
                r.accumulative_total_costs,
                r.expected_profit
            ]

def custom_export_tasks(players):
    players = sorted(players, key=lambda p: (p.id_in_group))

    yield [
        'player_id', 'player_code', 'task1_d1', 'task1_d2', 'task1_d3', 'task1_d4', 'task1_d5',
        'task1_d6', 'task1_d7', 'task1_d8', 'task1_d9', 'task1_d10',
        'task1_selected_decision', 'task1_random_number', 'task1_payoff',
        'task2_g1', 'task2_g2', 'task2_g3', 'task2_g4', 'task2_g5', 'task2_g6',
        'task2_selected_gamble', 'task2_outcome', 'task2_payoff',
    ]
    for p in players:
        if p.task1_selected_decision is not None:
            yield [
                p.id_in_group,
                p.participant.code,
                p.task1_d1,
                p.task1_d2,
                p.task1_d3,
                p.task1_d4,
                p.task1_d5,
                p.task1_d6,
                p.task1_d7,
                p.task1_d8,
                p.task1_d9,
                p.task1_d10,
                p.task1_selected_decision,
                p.task1_random_number,
                p.task1_payoff,
                p.task2_g1,
                p.task2_g2,
                p.task2_g3,
                p.task2_g4,
                p.task2_g5,
                p.task2_g6,
                p.task2_selected_gamble,
                p.task2_outcome,
                p.task2_payoff,
            ]


def custom_export_time_tracking(players):
    # Filter to only include last round players with duration data
    last_round_players = [p for p in players if p.round_number == C.NUM_ROUNDS]
    last_round_players = sorted(last_round_players, key=lambda p: p.id_in_group)

    yield [
        'player_id',
        'player_code',
        'welcoming_duration',
        'instruction1_duration',
        'instruction2_duration',
        'payment_duration',
        'question_duration',
        'game_duration',
        'game_result_duration',
        'extra_task1_duration',
        'extra_task2_duration',
        'extra_task_result_duration',
        'demographic_duration',
        'total_duration',
        'total_duration_excluding_results',
    ]

    for p in last_round_players:
        # Export if any duration field has been calculated (demographic page has been completed)
        if (p.total_duration or 0) > 0 or (p.demographic_duration or 0) > 0:
            yield [
                p.id_in_group,
                p.participant.code,
                p.welcoming_duration,
                p.instruction1_duration,
                p.instruction2_duration,
                p.payment_duration,
                p.question_duration,
                p.game_duration,
                p.game_result_duration,
                p.extra_task1_duration,
                p.extra_task2_duration,
                p.extra_task_result_duration,
                p.demographic_duration,
                p.total_duration,
                p.total_duration_excluding_results,
            ]


page_sequence = [WelcomingPage, InstructionPage1, InstructionPage2, PaymentInfo, GamePage, GameResultPage, ExtraTask1, ExtraTask2, ExtraTaskResult, EndingPage]
