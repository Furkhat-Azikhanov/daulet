from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# Список из 25 вопросов с вариантами ответов и их значениями
questions = [
    {
        "question": "Представьте, что вам дали задачу проанализировать данные, но не дали инструкции. Вы:",
        "options": [
            {"text": "Начнёте искать в интернете подходы к анализу.", "profile": "Аналитический", "points": 1},
            {"text": "Будете экспериментировать, пока не найдёте решение.", "profile": "Технический", "points": 4},
            {"text": "Попросите коллег объяснить задачу подробнее.", "profile": "Социальный", "points": 3}
        ]
    },
    {
        "question": "Во время обсуждения проекта кто-то высказывает идею, с которой вы не согласны. Ваша реакция:",
        "options": [
            {"text": "Предлагаете свою точку зрения с доказательствами.", "profile": "Аналитический", "points": 1},
            {"text": "Сначала выслушаете, а потом обдумаете.", "profile": "Управленческий", "points": 5},
            {"text": "Предпочтёте просто наблюдать за дальнейшим обсуждением.", "profile": "Социальный", "points": 3}
        ]
    },
    {
        "question": "Вам предложили сложную таблицу данных без объяснений, как её использовать. Ваши действия:",
        "options": [
            {"text": "Постараетесь понять структуру таблицы и искать закономерности.", "profile": "Аналитический", "points": 1},
            {"text": "Попробуете сделать гипотезы на основе цифр.", "profile": "Технический", "points": 4},
            {"text": "Попросите у других примеры или аналогии.", "profile": "Социальный", "points": 3}
        ]
    },
    {
        "question": "Если бы у вас была возможность создать отчёт о сложном проекте, как бы вы к нему подошли?",
        "options": [
            {"text": "Используете готовые шаблоны и фреймворки.", "profile": "Аналитический", "points": 1},
            {"text": "Придумаете свой уникальный способ представления данных.", "profile": "Творческий", "points": 2},
            {"text": "Обсудите варианты с командой, чтобы выбрать наилучший подход.", "profile": "Управленческий", "points": 5}
        ]
    },
    {
        "question": "Ваше отношение к правилам, с которыми вы не согласны?",
        "options": [
            {"text": "Оставляете их без внимания.", "profile": "Аналитический", "points": 1},
            {"text": "Анализируете и пытаетесь изменить через аргументацию.", "profile": "Управленческий", "points": 5},
            {"text": "Придерживаетесь правил, но помните про их недостатки.", "profile": "Социальный", "points": 3}
        ]
    },
    {
        "question": "Если вам предложат создать уникальный проект, который должен быть запоминающимся, ваша реакция:",
        "options": [
            {"text": "Возьмётесь, если дадут чёткие рамки.", "profile": "Управленческий", "points": 5},
            {"text": "Почувствуете вдохновение и сразу начнёте придумывать концепцию.", "profile": "Творческий", "points": 2},
            {"text": "Поделитесь идеей с коллегами и спросите их мнение.", "profile": "Социальный", "points": 3}
        ]
    },
    {
        "question": "На пустой стене перед вами можно нарисовать что угодно. Вы:",
        "options": [
            {"text": "Сначала подумаете, что бы подошло сюда лучше всего.", "profile": "Аналитический", "points": 1},
            {"text": "Сразу начнёте рисовать, не задумываясь.", "profile": "Творческий", "points": 2},
            {"text": "Спросите, чего хотят другие, а потом добавите что-то от себя.", "profile": "Социальный", "points": 3}
        ]
    },
    {
        "question": "Вас попросили создать презентацию для большой аудитории, как вы к этому подойдёте?",
        "options": [
            {"text": "Исследуете успешные примеры для вдохновения.", "profile": "Управленческий", "points": 5},
            {"text": "Будете экспериментировать с разными стилями, пока не найдёте подходящий.", "profile": "Творческий", "points": 2},
            {"text": "Сконсультируетесь с коллегами о том, что им больше нравится.", "profile": "Социальный", "points": 3}
        ]
    },
    {
        "question": "Если в задании есть риск, что его не примут, вы:",
        "options": [
            {"text": "Предпочтёте проработать максимально креативный вариант.", "profile": "Творческий", "points": 2},
            {"text": "Обдумаете баланс между стандартным и новым.", "profile": "Управленческий", "points": 5},
            {"text": "Оставите основной вариант и добавите к нему несколько идей.", "profile": "Аналитический", "points": 1}
        ]
    },
    {
        "question": "Если бы вам предложили выбрать, как провести день, то как бы вы организовали его:",
        "options": [
            {"text": "У вас сразу появится несколько идей, куда пойти.", "profile": "Творческий", "points": 2},
            {"text": "Вы организуете несколько занятий, оставив время для спонтанных решений.", "profile": "Социальный", "points": 3},
            {"text": "Предпочтёте спланировать всё и действовать по графику.", "profile": "Технический", "points": 4}
        ]
    },
    {
        "question": "Если к вам обратится незнакомый человек с просьбой, какова ваша реакция?",
        "options": [
            {"text": "Сначала обдумаете, чем ему можно помочь.", "profile": "Социальный", "points": 3},
            {"text": "Включитесь в помощь, ориентируясь на ситуацию.", "profile": "Управленческий", "points": 5},
            {"text": "Сначала подумаете, нужно ли это вам, прежде чем помогать.", "profile": "Технический", "points": 4}
        ]
    },
    {
        "question": "На совещании часто бывают конфликты. Вы:",
        "options": [
            {"text": "Постараетесь сгладить острые углы и успокоить участников.", "profile": "Социальный", "points": 3},
            {"text": "Попробуете найти причины конфликтов и договориться с участниками.", "profile": "Управленческий", "points": 5},
            {"text": "Будете наблюдать за дискуссией, избегая вмешательства.", "profile": "Технический", "points": 4}
        ]
    },
    {
        "question": "Если вам предложат обучить новичков, вы:",
        "options": [
            {"text": "Сначала определите, что им будет полезно.", "profile": "Социальный", "points": 3},
            {"text": "Начнёте с объяснений, которые легко запомнить.", "profile": "Творческий", "points": 2},
            {"text": "Предпочтёте коротко изложить основы и дать больше свободы.", "profile": "Управленческий", "points": 5}
        ]
    },
    {
        "question": "Вас просят организовать встречу с большой группой, вы:",
        "options": [
            {"text": "Сразу предлагаете темы и организацию.", "profile": "Управленческий", "points": 5},
            {"text": "Попросите всех участвовать, чтобы встреча была продуктивной.", "profile": "Социальный", "points": 3},
            {"text": "Составите график, оставив время для обсуждений.", "profile": "Технический", "points": 4}
        ]
    },
    {
        "question": "При обсуждении разных мнений вы:",
        "options": [
            {"text": "Постараетесь услышать все стороны.", "profile": "Социальный", "points": 3},
            {"text": "Попробуете найти компромиссное решение.", "profile": "Управленческий", "points": 5},
            {"text": "Сфокусируетесь на наиболее логичных идеях.", "profile": "Аналитический", "points": 1}
        ]
    },
    {
        "question": "Какой подход вы выбрали бы для точной задачи?",
        "options": [
            {"text": "Используете привычные методы.", "profile": "Технический", "points": 4},
            {"text": "Поэкспериментируете, чтобы найти оптимальное решение.", "profile": "Аналитический", "points": 1},
            {"text": "Обратитесь к проверенным источникам.", "profile": "Управленческий", "points": 5}
        ]
    },
{
        "question": "Какой формат работы вам ближе: командный или одиночный?",
        "options": [
            {"text": "Командный, чтобы обсуждать и улучшать идеи.", "profile": "Социальный", "points": 3},
            {"text": "Одиночный, чтобы сконцентрироваться на задаче.", "profile": "Технический", "points": 4},
            {"text": "Сначала одиночный, а потом командный.", "profile": "Управленческий", "points": 5}
        ]
    },
    {
        "question": "Вам дают задачу, требующую высокой точности, как вы её решите?",
        "options": [
            {"text": "Проверите несколько раз перед сдачей.", "profile": "Аналитический", "points": 1},
            {"text": "Сконцентрируетесь на технике выполнения.", "profile": "Технический", "points": 4},
            {"text": "Найдёте способ автоматизировать часть работы.", "profile": "Управленческий", "points": 5}
        ]
    },
    {
        "question": "Если бы вам предложили систематическую работу, вы:",
        "options": [
            {"text": "Примете её, если можно будет улучшить процессы.", "profile": "Аналитический", "points": 1},
            {"text": "Предпочтёте более вариативные задачи.", "profile": "Творческий", "points": 2},
            {"text": "Примете, так как любите порядок.", "profile": "Технический", "points": 4}
        ]
    },
    {
        "question": "В случае проблем с техникой или оборудованием вы:",
        "options": [
            {"text": "Будете искать причину и пробовать разные решения.", "profile": "Технический", "points": 4},
            {"text": "Найдёте нужные инструкции и внимательно их изучите.", "profile": "Управленческий", "points": 5},
            {"text": "Попробуете справиться самостоятельно, прежде чем звать специалиста.", "profile": "Социальный", "points": 3}
        ]
    },
    {
        "question": "Если в команде возникает спор, ваша роль:",
        "options": [
            {"text": "Пытаетесь успокоить и найти компромисс.", "profile": "Социальный", "points": 3},
            {"text": "Сформулируете чёткие решения и порядок.", "profile": "Управленческий", "points": 5},
            {"text": "Будете наблюдать и выскажетесь в конце.", "profile": "Аналитический", "points": 1}
        ]
    },
    {
        "question": "Какой стиль работы вам ближе?",
        "options": [
            {"text": "Плавный и организованный.", "profile": "Социальный", "points": 3},
            {"text": "Варьирующийся в зависимости от задач.", "profile": "Творческий", "points": 2},
            {"text": "Постоянно планируемый и контролируемый.", "profile": "Управленческий", "points": 5}
        ]
    },
    {
        "question": "Если бы вам предложили увеличить доход компании, вы:",
        "options": [
            {"text": "Постараетесь найти нестандартные пути.", "profile": "Творческий", "points": 2},
            {"text": "Придёте с логическим подходом и планом.", "profile": "Управленческий", "points": 5},
            {"text": "Начнёте анализировать рынок и конкурентов.", "profile": "Аналитический", "points": 1}
        ]
    },
    {
        "question": "Вам нужно провести собрание по важной теме. Как вы это организуете?",
        "options": [
            {"text": "Придумайте увлекательную концепцию встречи.", "profile": "Творческий", "points": 2},
            {"text": "Начнёте с подготовки материалов и данных.", "profile": "Аналитический", "points": 1},
            {"text": "Оставите место для дискуссий и обратной связи.", "profile": "Управленческий", "points": 5}
        ]
    },
    {
        "question": "Какой подход в организации делегирования вам ближе?",
        "options": [
            {"text": "Выборочные задачи отдаёте команде.", "profile": "Социальный", "points": 3},
            {"text": "Большинство задач оставляете за собой.", "profile": "Технический", "points": 4},
            {"text": "Предпочитаете делегировать, если есть возможность контроля.", "profile": "Управленческий", "points": 5}
        ]
    }
]

# Корневой маршрут перенаправляет на тест
@app.route('/')
def index():
    return redirect(url_for('test'))

# Страница с тестом (вопросами)
@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'answers' not in session:
        session['answers'] = []
    
    question_number = len(session['answers'])
    if question_number < len(questions):
        question_data = questions[question_number]
        return render_template("question.html", question_data=question_data, question_number=question_number + 1)
    else:
        return redirect(url_for('results'))

# Обработка ответа
@app.route('/answer', methods=['POST'])
def answer():
    selected_option = int(request.form['answer'])
    session['answers'].append(selected_option)
    return redirect(url_for('test'))

# Страница с результатами
@app.route('/results')
def results():
    profiles = {"Аналитический": 0, "Творческий": 0, "Социальный": 0, "Технический": 0, "Управленческий": 0}
    
    for i, answer in enumerate(session['answers']):
        option = questions[i]['options'][answer]
        profile = option.get('profile')
        points = option.get('points', 0)
        
        if profile:
            profiles[profile] += points

    profile = max(profiles, key=profiles.get)
    profile_description = get_profile_description(profile)
    recommended_courses = get_recommended_courses(profile)

    session.pop('answers', None)

    return render_template("result.html", profile=profile, profile_description=profile_description, recommended_courses=recommended_courses)

# Функции описания профилей и рекомендованных курсов остаются без изменений
def get_profile_description(profile):
    descriptions = {
        "Аналитический": "Вы обладаете выдающимися способностями к анализу и решению сложных задач...",
        "Творческий": "Вы склонны к поиску нестандартных решений и реализации идей...",
        "Социальный": "Вы умеете находить общий язык с людьми и решать конфликты...",
        "Технический": "Вас привлекают точные науки и задачи, требующие внимательности...",
        "Управленческий": "Вы обладаете лидерскими качествами и стремитесь к координации и руководству..."
    }
    return descriptions.get(profile, "")

def get_recommended_courses(profile):
    courses = {
        "Аналитический": [
            {"course": "Перейти к результату для аналитического профиля", "link": "http://jastarsb.tilda.ws/rezultat-analitik"}
        ],
        "Творческий": [
            {"course": "Перейти к результату для творческого профиля", "link": "http://jastarsb.tilda.ws/rezultat-tvorcheskij"}
        ],
        "Социальный": [
            {"course": "Перейти к результату для социального профиля", "link": "http://jastarsb.tilda.ws/rezultat-socialnyj"}
        ],
        "Технический": [
            {"course": "Перейти к результату для технического профиля", "link": "http://jastarsb.tilda.ws/rezultat-tekhnicheskij"}
        ],
        "Управленческий": [
            {"course": "Перейти к результату для управленческого профиля", "link": "https://jastarsb.tilda.ws/rezultat-upravlencheskij"}
        ]
    }
    return courses.get(profile, [])

if __name__ == '__main__':
    app.run(debug=True)
