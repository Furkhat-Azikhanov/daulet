from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

questions = [
    # Вопросы для аналитического профиля
    {
        "question": "Представьте, что вам дали задачу проанализировать данные, но не дали инструкции. Вы:",
        "options": [
            {"text": "Начнёте искать в интернете подходы к анализу.", "value": 1},
            {"text": "Будете экспериментировать, пока не найдёте решение.", "value": 1},
            {"text": "Попросите коллег объяснить задачу подробнее.", "value": 1}
        ]
    },
    {
        "question": "Во время обсуждения проекта кто-то высказывает идею, с которой вы не согласны. Ваша реакция:",
        "options": [
            {"text": "Предлагаете свою точку зрения с доказательствами.", "value": 1},
            {"text": "Сначала выслушаете, а потом обдумаете.", "value": 1},
            {"text": "Предпочтёте просто наблюдать за дальнейшим обсуждением.", "value": 1}
        ]
    },
    {
        "question": "Вам предложили сложную таблицу данных без объяснений, как её использовать. Ваши действия:",
        "options": [
            {"text": "Постараетесь понять структуру таблицы и искать закономерности.", "value": 1},
            {"text": "Попробуете сделать гипотезы на основе цифр.", "value": 1},
            {"text": "Попросите у других примеры или аналогии.", "value": 1}
        ]
    },
    {
        "question": "Если бы у вас была возможность создать отчёт о сложном проекте, как бы вы к нему подошли?",
        "options": [
            {"text": "Используете готовые шаблоны и фреймворки.", "value": 1},
            {"text": "Придумаете свой уникальный способ представления данных.", "value": 1},
            {"text": "Обсудите варианты с командой, чтобы выбрать наилучший подход.", "value": 1}
        ]
    },
    {
        "question": "Ваше отношение к правилам, с которыми вы не согласны?",
        "options": [
            {"text": "Оставляете их без внимания.", "value": 1},
            {"text": "Анализируете и пытаетесь изменить через аргументацию.", "value": 1},
            {"text": "Придерживаетесь правил, но помните про их недостатки.", "value": 1}
        ]
    },

    # Вопросы для творческого профиля
    {
        "question": "Если вам предложат создать уникальный проект, который должен быть запоминающимся, ваша реакция:",
        "options": [
            {"text": "Возьмётесь, если дадут чёткие рамки.", "value": 2},
            {"text": "Почувствуете вдохновение и сразу начнёте придумывать концепцию.", "value": 2},
            {"text": "Поделитесь идеей с коллегами и спросите их мнение.", "value": 2}
        ]
    },
    {
        "question": "На пустой стене перед вами можно нарисовать что угодно. Вы:",
        "options": [
            {"text": "Сначала подумаете, что бы подошло сюда лучше всего.", "value": 2},
            {"text": "Сразу начнёте рисовать, не задумываясь.", "value": 2},
            {"text": "Спросите, чего хотят другие, а потом добавите что-то от себя.", "value": 2}
        ]
    },
    {
        "question": "Вас попросили создать презентацию для большой аудитории, как вы к этому подойдёте?",
        "options": [
            {"text": "Исследуете успешные примеры для вдохновения.", "value": 2},
            {"text": "Будете экспериментировать с разными стилями, пока не найдёте подходящий.", "value": 2},
            {"text": "Сконсультируетесь с коллегами о том, что им больше нравится.", "value": 2}
        ]
    },
    {
        "question": "Если в задании есть риск, что его не примут, вы:",
        "options": [
            {"text": "Предпочтёте проработать максимально креативный вариант.", "value": 2},
            {"text": "Обдумаете баланс между стандартным и новым.", "value": 2},
            {"text": "Оставите основной вариант и добавите к нему несколько идей.", "value": 2}
        ]
    },
    {
        "question": "Если бы вам предложили выбрать, как провести день, то как бы вы организовали его:",
        "options": [
            {"text": "У вас сразу появится несколько идей, куда пойти.", "value": 2},
            {"text": "Вы организуете несколько занятий, оставив время для спонтанных решений.", "value": 2},
            {"text": "Предпочтёте спланировать всё и действовать по графику.", "value": 2}
        ]
    },

    # Вопросы для социального профиля
    {
        "question": "Если к вам обратится незнакомый человек с просьбой, какова ваша реакция?",
        "options": [
            {"text": "Сначала обдумаете, чем ему можно помочь.", "value": 3},
            {"text": "Включитесь в помощь, ориентируясь на ситуацию.", "value": 3},
            {"text": "Сначала подумаете, нужно ли это вам, прежде чем помогать.", "value": 3}
        ]
    },
    {
        "question": "На совещании часто бывают конфликты. Вы:",
        "options": [
            {"text": "Постараетесь сгладить острые углы и успокоить участников.", "value": 3},
            {"text": "Попробуете найти причины конфликтов и договориться с участниками.", "value": 3},
            {"text": "Будете наблюдать за дискуссией, избегая вмешательства.", "value": 3}
        ]
    },
    {
        "question": "Если вам предложат обучить новичков, вы:",
        "options": [
            {"text": "Сначала определите, что им будет полезно.", "value": 3},
            {"text": "Начнёте с объяснений, которые легко запомнить.", "value": 3},
            {"text": "Предпочтёте коротко изложить основы и дать больше свободы.", "value": 3}
        ]
    },
    {
        "question": "Вас просят организовать встречу с большой группой, вы:",
        "options": [
            {"text": "Сразу предлагаете темы и организацию.", "value": 3},
            {"text": "Попросите всех участвовать, чтобы встреча была продуктивной.", "value": 3},
            {"text": "Составите график, оставив время для обсуждений.", "value": 3}
        ]
    },
    {
        "question": "При обсуждении разных мнений вы:",
        "options": [
            {"text": "Постараетесь услышать все стороны.", "value": 3},
            {"text": "Попробуете найти компромиссное решение.", "value": 3},
            {"text": "Сфокусируетесь на наиболее логичных идеях.", "value": 3}
        ]
    },

    # Вопросы для технического профиля
    {
        "question": "Какой подход вы выбрали бы для точной задачи?",
        "options": [
            {"text": "Используете привычные методы.", "value": 4},
            {"text": "Поэкспериментируете, чтобы найти оптимальное решение.", "value": 4},
            {"text": "Обратитесь к проверенным источникам.", "value": 4}
        ]
    },
    {
        "question": "Какой формат работы вам ближе: командный или одиночный?",
        "options": [
            {"text": "Командный, чтобы обсуждать и улучшать идеи.", "value": 4},
            {"text": "Одиночный, чтобы сконцентрироваться на задаче.", "value": 4},
            {"text": "Сначала одиночный, а потом командный.", "value": 4}
        ]
    },
    {
        "question": "Вам дают задачу, требующую высокой точности, как вы её решите?",
        "options": [
            {"text": "Проверите несколько раз перед сдачей.", "value": 4},
            {"text": "Сконцентрируетесь на технике выполнения.", "value": 4},
            {"text": "Найдёте способ автоматизировать часть работы.", "value": 4}
        ]
    },
    {
        "question": "Если бы вам предложили систематическую работу, вы:",
        "options": [
            {"text": "Примете её, если можно будет улучшить процессы.", "value": 4},
            {"text": "Предпочтёте более вариативные задачи.", "value": 4},
            {"text": "Примете, так как любите порядок.", "value": 4}
        ]
    },
    {
        "question": "В случае проблем с техникой или оборудованием вы:",
        "options": [
            {"text": "Будете искать причину и пробовать разные решения.", "value": 4},
            {"text": "Найдёте нужные инструкции и внимательно их изучите.", "value": 4},
            {"text": "Попробуете справиться самостоятельно, прежде чем звать специалиста.", "value": 4}
        ]
    },

    # Вопросы для управленческого профиля
    {
        "question": "Если в команде возникает спор, ваша роль:",
        "options": [
            {"text": "Пытаетесь успокоить и найти компромисс.", "value": 5},
            {"text": "Сформулируете чёткие решения и порядок.", "value": 5},
            {"text": "Будете наблюдать и выскажетесь в конце.", "value": 5}
        ]
    },
    {
        "question": "Какой стиль работы вам ближе?",
        "options": [
            {"text": "Плавный и организованный.", "value": 5},
            {"text": "Варьирующийся в зависимости от задач.", "value": 5},
            {"text": "Постоянно планируемый и контролируемый.", "value": 5}
        ]
    },
    {
        "question": "Если бы вам предложили увеличить доход компании, вы:",
        "options": [
            {"text": "Постараетесь найти нестандартные пути.", "value": 5},
            {"text": "Придёте с логическим подходом и планом.", "value": 5},
            {"text": "Начнёте анализировать рынок и конкурентов.", "value": 5}
        ]
    },
    {
        "question": "Вам нужно провести собрание по важной теме. Как вы это организуете?",
        "options": [
            {"text": "Придумаете увлекательную концепцию встречи.", "value": 5},
            {"text": "Начнёте с подготовки материалов и данных.", "value": 5},
            {"text": "Оставите место для дискуссий и обратной связи.", "value": 5}
        ]
    },
    {
        "question": "Какой подход в организации делегирования вам ближе?",
        "options": [
            {"text": "Выборочные задачи отдаёте команде.", "value": 5},
            {"text": "Большинство задач оставляете за собой.", "value": 5},
            {"text": "Предпочитаете делегировать, если есть возможность контроля.", "value": 5}
        ]
    }
]



# Главная страница - перенаправление на сайт на Tilda
@app.route('/')
def index():
    return redirect("https://tilda.project.url")  # ссылка на главную страницу на Tilda

# Начало теста, переход к первому вопросу
@app.route('/test')
def start_test():
    session['answers'] = []  # очищаем ответы
    session['current_question'] = 0  # устанавливаем начальный вопрос
    return redirect(url_for('question'))

# Показ текущего вопроса
@app.route('/question', methods=['GET', 'POST'])
def question():
    # Получаем текущий индекс вопроса
    current_question = session.get('current_question', 0)

    # Сохраняем ответ на предыдущий вопрос
    if request.method == 'POST':
        answer = int(request.form.get('answer'))
        session['answers'].append(answer)
        session['current_question'] = current_question + 1

    # Если вопросы закончились, переходим к результату
    if session['current_question'] >= len(questions):
        return redirect(url_for('result'))

    # Получаем текущий вопрос и варианты ответа
    question_data = questions[session['current_question']]
    return render_template('question.html', question_data=question_data, question_number=session['current_question'] + 1)

# Страница с результатом
@app.route('/result')
def result():
    # Подсчёт результата на основе ответов
    score = sum(session['answers'])
    profile, profile_description, recommended_courses = calculate_profile(score)
    return render_template('result.html', profile=profile, profile_description=profile_description, recommended_courses=recommended_courses)

# Функция для определения профиля
def calculate_profile(score):
    if score <= 25:
        return "Аналитический", "Вы обладаете аналитическим складом ума и способны решать сложные задачи...", [{"course": "Курс по аналитике данных"}]
    elif 26 <= score <= 50:
        return "Творческий", "Вы склонны к творческим решениям и уникальному подходу...", [{"course": "Курс по графическому дизайну"}]
    elif 51 <= score <= 75:
        return "Социальный", "Вы умеете находить общий язык с людьми и решать конфликты...", [{"course": "Курс по SMM"}]
    elif 76 <= score <= 100:
        return "Технический", "Вам близки задачи, требующие высокой точности и технических знаний...", [{"course": "Курс по программированию"}]
    else:
        return "Управленческий", "Вы обладаете лидерскими качествами и стремитесь к организации и координации...", [{"course": "Курс по управлению проектами"}]

if __name__ == '__main__':
    app.run(debug=True)