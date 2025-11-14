from otree.api import *
import random


doc = """
Supply Chain Resilience Spending Game - Test Version
"""


class C(BaseConstants):
    NAME_IN_URL = 'experiment_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    INITIAL_PROFIT = 10000 #(base) total profit for 100 rounds
    GROSS_PROFIT = 100 #(base) gross profit every round
    DISRUPTION_COST = 2000 #(base) disruption impact
    BASIC_PROBABILITY = 5 #(base) disruption probability
    SHOW_UP_FEE = 3
    CONVERSION_RATE = 1 / 1500


    # Comprehension Questions - 8 Multiple Choice Questions
    COMP_QUESTIONS_MC = [
        {
            'question': 'How many Rounds do you play in this experiment?',
            'options': [
                {'text': '20 rounds'},
                {'text': '100 rounds', 'correct': True},
                {'text': '120 rounds'}
            ]
        },
        {
            'question': 'How much Gross profit do you earn each round?',
            'options': [
                {'text': '1000 ECU'},
                {'text': '100 ECU', 'correct': True},
                {'text': '200 ECU'}
            ]
        },
        {
            'question': 'What is the Probability of disruptions when your SC resilience spending is zero?',
            'options': [
                {'text': '5%', 'correct': True},
                {'text': '4%'},
                {'text': '4.5%'}
            ]
        },
        {
            'question': 'What is the Impact of disruptions when your SC resilience spending is zero?',
            'options': [
                {'text': '1000 ECU'},
                {'text': '2000 ECU', 'correct': True},
                {'text': '100 ECU'}
            ]
        },
        {
            'question': 'What is your Profit when you spend 20 ECU on SC resilience and no disruption occurs?',
            'options': [
                {'text': '80 ECU', 'correct': True},
                {'text': '-20 ECU'},
                {'text': '-120 ECU'}
            ]
        },
        {
            'question': 'What is the Maximum amount of spending you can make?',
            'options': [
                {'text': '50 ECU'},
                {'text': '2000 ECU'},
                {'text': '100 ECU', 'correct': True}
            ]
        },
        {
            'question': 'What is the Probability of disruptions when your SC resilience spending is 100 ECU?',
            'options': [
                {'text': '5%'},
                {'text': '0%', 'correct': True},
                {'text': '0.5%'}
            ]
        },
        {
            'question': 'What is the Impact of disruptions when your SC resilience spending is 100 ECU?',
            'options': [
                {'text': '2000 ECU'},
                {'text': '100 ECU'},
                {'text': '0 ECU', 'correct': True}
            ]
        }
    ]

    # Comprehension Questions - 2 True/False Questions
    COMP_QUESTIONS_TF = [
        {
            'question': 'You can decide to spend on SC resilience freely between 0 and 100.',
            'options': [
                {'text': 'True', 'correct': True},
                {'text': 'False'}
            ]
        },
        {
            'question': 'After spending 50 ECU on SC resilience, you can also be at risk of disruptions.',
            'options': [
                {'text': 'True', 'correct': True},
                {'text': 'False'}
            ]
        }
    ]

    # Demographic questionnaire
    BIRTH_YEARS = list(range(1980, 2011))  # 1980 to 2010

    GENDER_CHOICES = [
        ['male', 'Male'],
        ['female', 'Female'],
        ['other', 'Other'],
        ['prefer_not', 'Prefer not to say']
    ]

    ETHNICITY_CHOICES = [
        ['asian', 'Asian'],
        ['european', 'European'],
        ['african', 'African'],
        ['american', 'American'],
        ['latin_american', 'Latin American'],
        ['mixed', 'Mixed background']
    ]

    EDUCATION_CHOICES = [
        ['first_year', 'First-year undergraduate student'],
        ['second_year', 'Second-year undergraduate student'],
        ['third_final', 'Third-year/final-year undergraduate student'],
        ['masters', 'Masters student'],
        ['doctoral', 'Doctoral/PhD student']
    ]

    SCR_IMPORTANCE_CHOICES = [
        [1, '1'],
        [2, '2'],
        [3, '3'],
        [4, '4'],
        [5, '5'],
        [6, '6'],
        [7, '7']
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Spending Game fields
    money_input = models.IntegerField(min=0, max=100, label="", blank=False)
    is_disrupted = models.BooleanField(initial=False)
    cost_of_disruption = models.IntegerField(initial=0)
    total_costs = models.IntegerField(initial=0)
    expected_profit = models.IntegerField(initial=C.INITIAL_PROFIT)
    round_calculated = models.BooleanField(initial=False)

    # Comprehension question fields
    def make_field():
        return models.StringField(
            blank=True,
            choices=[['a', 'a'], ['b', 'b'], ['c', 'c']],
            widget=widgets.RadioSelect
        )

    # Comprehension questions - 5 random questions drawn from 10
    comp_q1 = make_field()
    comp_q2 = make_field()
    comp_q3 = make_field()
    comp_q4 = make_field()
    comp_q5 = make_field()
    question_attempts = models.IntegerField(initial=0)
    question_failed = models.BooleanField(initial=False)
    current_question_indices = models.StringField(initial='')

    # Extra task 1 fields - 10 decisions
    task1_d1 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d2 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d3 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d4 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d5 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d6 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d7 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d8 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d9 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d10 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_selected_decision = models.IntegerField()
    task1_random_number = models.IntegerField()
    task1_payoff = models.IntegerField()

    # Extra task 2 fields - 6 gambles
    task2_g1 = models.StringField(choices=[['Accept', 'Accept'], ['Reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g2 = models.StringField(choices=[['Accept', 'Accept'], ['Reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g3 = models.StringField(choices=[['Accept', 'Accept'], ['Reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g4 = models.StringField(choices=[['Accept', 'Accept'], ['Reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g5 = models.StringField(choices=[['Accept', 'Accept'], ['Reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g6 = models.StringField(choices=[['Accept', 'Accept'], ['Reject', 'Reject']], widget=widgets.RadioSelect)
    task2_selected_gamble = models.IntegerField()
    task2_outcome = models.IntegerField()
    task2_payoff = models.IntegerField()

    # Demographic questionnaire fields - 5 questions
    birth_year = models.IntegerField(
        label="What is your year of birth?",
        choices=[[year, str(year)] for year in C.BIRTH_YEARS],
        blank=False
    )
    gender = models.StringField(
        label="What is your gender?",
        choices=C.GENDER_CHOICES,
        widget=widgets.RadioSelect,
        blank=False
    )
    ethnicity = models.StringField(
        label="Which of the following options best describes your ethnic background?",
        choices=C.ETHNICITY_CHOICES,
        widget=widgets.RadioSelect,
        blank=False
    )
    education_status = models.StringField(
        label="Which of the following options best describes your current educational status?",
        choices=C.EDUCATION_CHOICES,
        widget=widgets.RadioSelect,
        blank=False
    )
    scr_importance = models.IntegerField(
        label="Please indicate the extent to which you think Supply Chain Resilience (or Supply Chain Risk Management) is important nowadays?",
        choices=C.SCR_IMPORTANCE_CHOICES,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )


class CombinedResult(ExtraModel):
    player = models.Link(Player)
    spending = models.IntegerField()
    is_disrupted = models.BooleanField()
    cost_of_disruption = models.IntegerField()
    total_costs = models.IntegerField(initial=0)
    expected_profit = models.IntegerField(initial=C.INITIAL_PROFIT)


# PAGES
class WelcomingPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class QuestionPage(Page):
    form_model = 'player'
    form_fields = ['comp_q1', 'comp_q2', 'comp_q3', 'comp_q4', 'comp_q5']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not player.question_failed

    @staticmethod
    def vars_for_template(player: Player):
        attempt_number = player.question_attempts + 1
        # Select 4 random questions from 8 multiple choice questions
        mc_indices = random.sample(range(len(C.COMP_QUESTIONS_MC)), 4)

        # Select 1 random question from 2 True/False questions
        tf_index = random.randint(0, len(C.COMP_QUESTIONS_TF) - 1)

        # Get selected questions and shuffle their options
        selected_questions = []
        option_mappings = []

        # Process MC questions
        for i in mc_indices:
            original_q = C.COMP_QUESTIONS_MC[i]

            # Shuffle options
            shuffled_options = original_q['options'].copy()
            random.shuffle(shuffled_options)

            # Convert to dict format for template (a, b, c)
            options_dict = {}
            correct_key = None
            keys = ['a', 'b', 'c']

            for j, opt in enumerate(shuffled_options):
                options_dict[keys[j]] = opt['text']
                if opt.get('correct', False):
                    correct_key = keys[j]

            selected_questions.append({
                'question': original_q['question'],
                'options': options_dict,
            })

            option_mappings.append(correct_key)

        # Process TF question
        original_tf = C.COMP_QUESTIONS_TF[tf_index]

        # Shuffle True/False
        shuffled_tf = original_tf['options'].copy()
        random.shuffle(shuffled_tf)

        tf_options_dict = {}
        tf_correct_key = None

        for j, opt in enumerate(shuffled_tf):
            tf_options_dict[['a', 'b'][j]] = opt['text']
            if opt.get('correct', False):
                tf_correct_key = ['a', 'b'][j]

        selected_questions.append({
            'question': original_tf['question'],
            'options': tf_options_dict,
        })

        option_mappings.append(tf_correct_key)

        # Store indices and correct answer mappings for validation
        indices_str = ','.join(map(str, mc_indices)) + f',TF{tf_index}'
        mappings_str = ','.join(option_mappings)
        player.current_question_indices = indices_str + '|' + mappings_str

        return dict(
            questions=selected_questions,
            attempt_number=attempt_number,
        )

    @staticmethod
    def error_message(player: Player, values):
        # Check if all questions are answered
        unanswered = []
        for i in range(1, 6):
            field_name = f'comp_q{i}'
            if not values.get(field_name):
                unanswered.append(str(i))

        if unanswered:
            return "Please answer all questions before submitting"

        # Parse current question indices and mappings
        parts = player.current_question_indices.split('|')
        indices_str = parts[0]
        mappings_str = parts[1]

        correct_keys = mappings_str.split(',')

        # Check answers
        errors = []

        # Check all 5 questions using the stored correct keys
        for i in range(1, 6):
            field_name = f'comp_q{i}'
            if values[field_name] != correct_keys[i - 1]:
                errors.append(str(i))

        if errors:
            player.question_attempts += 1
            return f"Some answers are incorrect. Please try again. (Attempt {player.question_attempts + 1})"

class GamePage(Page):
    form_model = 'player'
    form_fields = ['money_input']

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return not player.question_failed
        return True

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
        if data['action'] == 'calculate_result':
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
                    prev_total_costs = prev_results[0].total_costs
                else:
                    prev_expected_profit = C.INITIAL_PROFIT
                    prev_total_costs = 0

                player.expected_profit = prev_expected_profit - spending - player.cost_of_disruption
                player.total_costs = prev_total_costs + spending + player.cost_of_disruption
            else:
                player.expected_profit = C.INITIAL_PROFIT - spending - player.cost_of_disruption
                player.total_costs = spending + player.cost_of_disruption

            existing_results = CombinedResult.filter(player=player)
            for result in existing_results:
                result.delete()

            CombinedResult.create(
                player=player,
                spending=spending,
                is_disrupted=player.is_disrupted,
                cost_of_disruption=player.cost_of_disruption,
                total_costs=player.total_costs,
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
                    'total_costs': player.total_costs,
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
                    prev_total_costs = prev_results[0].total_costs
                else:
                    prev_expected_profit = C.INITIAL_PROFIT
                    prev_total_costs = 0

                player.expected_profit = prev_expected_profit - spending - player.cost_of_disruption
                player.total_costs = prev_total_costs + spending + player.cost_of_disruption
            else:
                player.expected_profit = C.INITIAL_PROFIT - spending - player.cost_of_disruption
                player.total_costs = spending + player.cost_of_disruption

            existing_results = CombinedResult.filter(player=player)
            for result in existing_results:
                result.delete()

            CombinedResult.create(
                player=player,
                spending=spending,
                is_disrupted=player.is_disrupted,
                cost_of_disruption=player.cost_of_disruption,
                total_costs=player.total_costs,
                expected_profit=player.expected_profit,
            )


class GameResultPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).question_failed

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
        performance_payment = final_profit * C.CONVERSION_RATE
        performance_payment = round(performance_payment, 1)
        if performance_payment <= 0: performance_payment = 0

        # Calculate the total game payment
        total_payment = C.SHOW_UP_FEE + performance_payment
        total_payment = round(total_payment, 1)

        player.participant.payoff = total_payment

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


class ExtraTask1(Page):
    form_model = 'player'
    form_fields = ['task1_d1', 'task1_d2', 'task1_d3', 'task1_d4', 'task1_d5',
                   'task1_d6', 'task1_d7', 'task1_d8', 'task1_d9', 'task1_d10']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).question_failed

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

class ExtraTask2 (Page):
    form_model = 'player'
    form_fields = ['task2_g1', 'task2_g2', 'task2_g3', 'task2_g4', 'task2_g5', 'task2_g6']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).question_failed

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.task2_selected_gamble = random.randint(1, 6)

        gamble_field = f'task2_g{player.task2_selected_gamble}'
        choice = getattr(player, gamble_field)

        gambles = {
            1: (-2000, 6000),
            2: (-3000, 6000),
            3: (-4000, 6000),
            4: (-5000, 6000),
            5: (-6000, 6000),
            6: (-7000, 6000),
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


class ExtraTaskResult(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).question_failed

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

        performance_payment = final_profit * C.CONVERSION_RATE
        performance_payment = round(performance_payment, 1)
        if performance_payment <= 0: performance_payment = 0
        spending_game_payment = C.SHOW_UP_FEE + performance_payment

        # Calculate tasks payment (convert ECU to Euro)
        task1_payment = round(player.task1_payoff * C.CONVERSION_RATE, 1)
        task2_payment = round(player.task2_payoff * C.CONVERSION_RATE, 1)
        tasks_total_payment = round(task1_payment + task2_payment, 1)

        # Total payment
        total_payment = round(spending_game_payment + tasks_total_payment, 1)
        player.participant.payoff = total_payment

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


class DemographicPage(Page):
    form_model = 'player'
    form_fields = ['birth_year', 'gender', 'ethnicity', 'education_status', 'scr_importance']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).question_failed


class EndingPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).question_failed

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
        performance_payment = final_profit * C.CONVERSION_RATE
        performance_payment = round(performance_payment, 1)
        if performance_payment <= 0: performance_payment = 0
        spending_game_payment = C.SHOW_UP_FEE + performance_payment

        # Calculate tasks payment
        task1_payment = round(player.task1_payoff * C.CONVERSION_RATE, 1)
        task2_payment = round(player.task2_payoff * C.CONVERSION_RATE, 1)
        tasks_total_payment = round(task1_payment + task2_payment, 1)

        # Total payment
        total_payment = round(spending_game_payment + tasks_total_payment, 1)

        # Get demographic data
        gender_labels = dict(C.GENDER_CHOICES)
        ethnicity_labels = dict(C.ETHNICITY_CHOICES)
        education_labels = dict(C.EDUCATION_CHOICES)

        return dict(
            # Spending game
            final_profit=final_profit,
            initial_profit=C.INITIAL_PROFIT,
            show_up_fee=C.SHOW_UP_FEE,
            performance_payment=performance_payment,
            spending_game_payment=spending_game_payment,

            # Task 1
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

            # Demographics
            birth_year=player.birth_year,
            gender=gender_labels.get(player.gender, player.gender) if player.gender else 'Not provided',
            ethnicity=ethnicity_labels.get(player.ethnicity, player.ethnicity) if player.ethnicity else 'Not provided',
            education_status=education_labels.get(player.education_status,
                                                  player.education_status) if player.education_status else 'Not provided',
            scr_importance=player.scr_importance if player.scr_importance else 'Not provided',
        )

def custom_export_game(players):
    players = sorted(players, key=lambda p: (p.id_in_group, p.round_number))

    yield [
        'player_id',
        'round_number',
        'spending',
        'is_disrupted',
        'cost_of_disruption',
        'total_costs',
        'expected_profit',
    ]

    for p in players:
        results = CombinedResult.filter(player=p)
        for r in results:
            yield [
                p.id_in_group,
                p.round_number,
                r.spending,
                1 if r.is_disrupted else 0,
                r.cost_of_disruption,
                r.total_costs,
                r.expected_profit
            ]

def custom_export_tasks(players):
    players = sorted(players, key=lambda p: (p.id_in_group))

    yield [
        'player_id', 'task1_d1', 'task1_d2', 'task1_d3', 'task1_d4', 'task1_d5',
        'task1_d6', 'task1_d7', 'task1_d8', 'task1_d9', 'task1_d10',
        'task1_selected_decision', 'task1_random_number', 'task1_payoff',
        'task2_g1', 'task2_g2', 'task2_g3', 'task2_g4', 'task2_g5', 'task2_g6',
        'task2_selected_gamble', 'task2_outcome', 'task2_payoff',
    ]
    for p in players:
        if p.task1_selected_decision is not None:
            yield [
                p.id_in_group,
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

def custom_export_demographics(players):
    players = sorted(players, key=lambda p: (p.id_in_group))

    yield [
        'player_id',
        'birth_year',
        'gender',
        'ethnicity',
        'education_status',
        'scr_importance',
    ]

    for p in players:
        if p.task1_selected_decision is not None:
            yield [
                p.id_in_group,
                p.birth_year,
                p.gender,
                p.ethnicity,
                p.education_status,
                p.scr_importance,
            ]


page_sequence = [WelcomingPage, QuestionPage, GamePage, GameResultPage, ExtraTask1, ExtraTask2, ExtraTaskResult, DemographicPage, EndingPage]
