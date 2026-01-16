import streamlit as st
import pandas as pd
import plotly.express as px  
import folium
from streamlit_folium import st_folium
import numpy as np

# --- НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="Digital Health Dashboard",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ФУНКЦІЯ ЗАВАНТАЖЕННЯ ДАНИХ ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/cleaned_data.csv')
    return df

df = load_data()

# --- БОКОВА ПАНЕЛЬ (SIDEBAR) ---
st.sidebar.title("🛠 Навігація")
page = st.sidebar.radio(
    "Оберіть розділ проєкту:",
    ["Головна", "Аналіз гіпотез", "Глобальна географія", "ML Діагностика", "Аналітичний звіт"]
)

st.sidebar.markdown("---")
st.sidebar.info("Проєкт підготував: Віталій Чернецький")

# --- ЛОГІКА ПЕРЕМИКАННЯ СТОРІНОК ---

if page == "Головна":
    st.title("📊 Аналіз залежності студентів від соціальних мереж")
    st.write("""
    Вітаємо у дослідницькому проєкті, присвяченому аналізу цифрових звичок молоді. 
    Ми дослідили дані 700+ студентів з усього світу, щоб зрозуміти, як екранний час 
    впливає на наше реальне життя.
    """)
    
    st.subheader("Ключові показники (Global Metrics)")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Респондентів", len(df))
    with col2:
        st.metric("Середній час в соцмережах", f"{df['Avg_Daily_Usage_Hours'].mean():.1f} год/добу")
    with col3:
        st.metric("Рівень залежності", f"{df['Addicted_Score'].mean():.1f}/з 10")
    with col4:
        st.metric("Регіонів", df['Region'].nunique())

    st.write("---")
    st.subheader("Попередній перегляд даних")
    st.dataframe(df.head(10), width='stretch')

elif page == "Аналіз гіпотез":
    st.title("🧬 Глибокий аналіз гіпотез")
    st.write("У цьому розділі ми перевіряємо статистичні припущення про вплив соцмереж на життя студентів.")

    # Створюємо закладки для різних груп гіпотез
    tab1, tab2, tab3, tab4 = st.tabs(["🏥 Здоров'я та Психіка", "📱 Платформи", "🤝 Соціальні зв'язки", "📖 Storytelling"])
    level_order = {"Addiction_Level": ["Low", "Medium", "High"]}

    with tab1:
        st.header("Вплив на фізичний та ментальний стан")
        
        st.subheader("Гіпотеза 1: Соцмережі та якість сну")
        fig1 = px.scatter(
            df, x="Avg_Daily_Usage_Hours", y="Sleep_Hours_Per_Night",
            color="Addiction_Level", trendline="ols",
            labels={"Avg_Daily_Usage_Hours": "Годин у мережі",
                    "Sleep_Hours_Per_Night": "Годин сну",
                    "Addiction_Level": "Рівень залежності"},
            color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"},
            category_orders=level_order
        )
        st.plotly_chart(fig1, width='stretch')
        st.success("**Висновок:** Чітка негативна кореляція. Зростання часу у соцмережах безпосередньо веде до скорочення тривалості сну.")

        st.write("---")

        st.subheader("Гіпотеза 2: Залежність та ментальний стан")
        fig2 = px.box(
            df, x="Addiction_Level", y="Mental_Health_Score",
            color="Addiction_Level", points="all",
            labels={"Addiction_Level": "Рівень залежності", "Mental_Health_Score": "Бал ментального здоров'я"},
            color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"},
            category_orders=level_order
        )
        st.plotly_chart(fig2, width='stretch')
        st.success("**Висновок:** Студенти з високим рівнем залежності мають значно нижчі медіанні показники ментального здоров'я.")

    with tab2:
        st.header("Аналіз за платформами")
        st.subheader("Гіпотеза 3: Платформи з алгоритмічною стрічкою vs Інші")
        
        platform_stats = df.groupby('Most_Used_Platform')['Addicted_Score'].mean().sort_values(ascending=False).reset_index()
        
        fig3 = px.bar(
            platform_stats, x="Most_Used_Platform", y="Addicted_Score",
            color="Addicted_Score",
            labels={"Most_Used_Platform": "Основна платформа", "Addicted_Score": "Середній бал залежності"},
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig3, width='stretch')
        st.info("**Аналітичний інсайт:** Платформи, що використовують алгоритми 'нескінченної стрічки' (TikTok, Instagram), мають найвищий статистичний зв'язок із балом залежності.")
        st.write("---")
        
        st.header("Аналіз за типами контенту")
        st.write("Ми згрупували платформи за їхньою основною функцією, щоб знайти 'дофамінові пастки'.")



        # 1. Скаттер-плот: Час в мережі vs Залежність
        st.subheader("⚡️ Співвідношення часу в мережі та адиктивності")
        
        type_stats = df.groupby('Platform_Type').agg({
            'Addicted_Score': 'mean',
            'Avg_Daily_Usage_Hours': 'mean',
            'Student_ID': 'count'
        }).reset_index()

        fig_scatter = px.scatter(
            type_stats, 
            x="Avg_Daily_Usage_Hours", 
            y="Addicted_Score",
            size="Student_ID", 
            color="Platform_Type",
            text="Platform_Type", # Підписи прямо на графіку
            labels={"Avg_Daily_Usage_Hours": "Сер. час використання (год)", 
                    "Addicted_Score": "Сер. бал залежності"},
            title="Де виникає найшвидша залежність?",
            height=500
        )

        # НАЛАШТУВАННЯ ВІЗУАЛУ
        fig_scatter.update_layout(
            showlegend=False,
            margin=dict(l=20, r=20, t=60, b=20) # Відступи для кращого вигляду
        )

        # Налаштування осей: фіксований крок 1.0 та вільний простір
        fig_scatter.update_xaxes(dtick=1.0, range=[2, 7])
        fig_scatter.update_yaxes(dtick=1.0, range=[3, 8])

        # Корекція тексту: щоб не налізав на бульбашки та не обрізався
        fig_scatter.update_traces(
            textposition='top center',
            cliponaxis=False
        )

        st.plotly_chart(fig_scatter, use_container_width=True)
        st.info("**Інсайт:** Категорія 'Entertain-Scroll' (TikTok/Instagram) має найвищу залежність, хоча в месенджерах проводять більше часу. Це доводить агресивність алгоритмів.")

        st.write("---")
        
        
        # 2. Гендерний розподіл за категоріями
        st.subheader("🚻 Хто і що обирає: Гендерний аспект")
        
        gender_data = df.groupby(['Platform_Type', 'Gender']).size().reset_index(name='Count')
        
        fig_gender = px.bar(
            gender_data, 
            x="Platform_Type", 
            y="Count", 
            color="Gender",
            barmode="group",
            labels={"Platform_Type": "Тип платформи", 
                    "Count": "Кількість"},
            title="Розподіл інтересів між чоловіками та жінками",
            color_discrete_map={"Male": "#1f77b4", "Female": "#e377c2"}
        )
        st.plotly_chart(fig_gender, use_container_width=True)
        st.warning("**Гендерний розрив:** Хлопці значно більше схильні до використання 'Social-Network' (новинних стрічок), тоді як дівчата домінують у розважальному контенті.\n\n"
                   "👉 Це вказує на різницю в цілях: хлопці йдуть за інформацією, дівчата — за візуальним контентом."
        )
        st.write("---")
        
        # 3. Ієрархічна структура: Категорії та Платформи
        st.subheader("🔍 Структура цифрового споживання")
        
        # Готуємо дані для Treemap
        tree_data = df.groupby(['Platform_Type', 'Most_Used_Platform']).agg({
            'Addicted_Score': 'mean',
            'Student_ID': 'count'
        }).reset_index()

        fig_tree = px.treemap(
            tree_data, 
            path=['Platform_Type', 'Most_Used_Platform'], # Створюємо ієрархію
            values='Student_ID', 
            color='Addicted_Score',
            color_continuous_scale='RdYlGn_r', # Від зеленого (низька) до червоного (висока)
            labels={'Student_ID': 'Кількість користувачів', 'Addicted_Score': 'Сер. бал залежності'},
            title="Популярність платформ у межах категорій (колір — рівень залежності)"
        )
        
        st.plotly_chart(fig_tree, use_container_width=True)
        st.info("Цей графік показує 'вагу' кожної платформи. Розмір прямокутника — це кількість студентів, а колір — наскільки ця платформа 'затягує'.")



    
    

    with tab3:
        st.header("Соціальні зв'язки та навчання")
        
        # --- Гіпотеза 4 ---
        st.subheader("Гіпотеза 4: Конфлікти та статус стосунків")
        conflict_stats = df.groupby('Relationship_Status')['Conflicts_Over_Social_Media'].mean().sort_values().reset_index()
        
        fig4 = px.bar(
            conflict_stats, 
            x="Conflicts_Over_Social_Media", 
            y="Relationship_Status",
            orientation='h',
            title="Середня частота конфліктів за статусом стосунків",
            labels={"Relationship_Status": "Статус стосунків", "Conflicts_Over_Social_Media": "Сер. кількість конфліктів"},
            color="Conflicts_Over_Social_Media", 
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig4, width='stretch')
        st.success("**Вердикт:** Гіпотеза підтверджена. Статус 'Complicated' демонструє найвищий рівень конфліктів через соціальні медіа.")
        
        st.write("---")

        # --- Гіпотеза 5 ---
        st.subheader("Гіпотеза 5: Стосунки як захисний фактор")
        fig6 = px.box(
            df, 
            x="Relationship_Status", 
            y="Addicted_Score",
            color="Relationship_Status",
            title="Розподіл рівня залежності за статусом стосунків",
            labels={"Relationship_Status": "Статус стосунків", "Addicted_Score": "Бал залежності"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig6, width='stretch')
        st.info("**Висновок:** Стабільні стосунки ('In a relationship') часто виступають стримуючим фактором, знижуючи середній рівень цифрової залежності.")

        st.write("---")
        
        # --- Гіпотеза 6 ---
        st.subheader("Гіпотеза 6: Вплив залежності на успішність")
        fig5 = px.box(
            df, x="Addiction_Level", y="Affects_Academic_Performance_Numeric",
            color="Addiction_Level",
            labels={
                "Addiction_Level": "Рівень залежності",
                "Affects_Academic_Performance_Numeric": "Вплив на успішність (числовий бал)"
            },
            color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"},
            category_orders=level_order
        )
        st.plotly_chart(fig5, width='stretch')
        st.success("**Вердикт:** Гіпотеза підтверджена — висока цифрова залежність статистично корелює зі зниженням академічної успішності.")

    

    with tab4:
        st.header("📖 Аналітичний звіт: Storytelling")
        
        try:
            # Відкриваємо та читаємо файл
            with open("STORYTELLING.md", "r", encoding="utf-8") as f:
                story_content = f.read()
            
            # Відображаємо вміст
            # unsafe_allow_html=True потрібен, якщо у вашому MD є HTML-теги (наприклад, для центрування картинок)
            st.markdown(story_content, unsafe_allow_html=True)
            
        except FileNotFoundError:
            st.error("Файл STORYTELLING.md не знайдено. Переконайтеся, що він лежить у корені проекту.")


elif page == "Глобальна географія":
    st.title("🌍 Глобальна географія залежності")
    st.write("Як цифрова залежність розподілена по світу?")

    # 1. Підготовка даних для карти
    # Рахуємо середній бал для кожної країни
    country_map_data = df.groupby('Country')['Addicted_Score'].mean().reset_index()

    # 2. Створення інтерактивної карти світу
    st.subheader("Світова карта рівня залежності")
    
    fig_map = px.choropleth(
        country_map_data,
        locations="Country",
        locationmode="country names",
        color="Addicted_Score",
        hover_name="Country",
        color_continuous_scale="YlOrRd", 
        labels={"Addicted_Score": "Сер. бал залежності"}
    )
    
    fig_map.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth' # Робимо карту візуально привабливішою
        ),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    st.plotly_chart(fig_map, width='stretch')

    st.write("---")

    # 3. Гіпотеза 7: Порівняння макрорегіонів
    st.subheader("Гіпотеза 7: Регіональні відмінності (Пн. Америка vs Європа)")
    
    # Використовуємо колонку Region, яку ми підготували під час очищення даних
    region_stats = df.groupby('Region')['Addicted_Score'].mean().sort_values(ascending=True).reset_index()
    
    fig_region = px.bar(
        region_stats,
        x="Addicted_Score",
        y="Region",
        orientation='h',
        color="Addicted_Score",
        text_auto='.2f', # Виводимо точне значення на стовпчиках
        title="Порівняння середнього рівня залежності за континентами",
        labels={"Region": "Континент", "Addicted_Score": "Середній бал"},
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_region, width='stretch')

    st.success("""
    **Вердикт:** Гіпотеза 7 підтверджена. Регіони з високою концентрацією технологічних хабів 
    (зокрема Північна Америка) демонструють вищі показники адиктивності порівняно з Європою.
    """)
    st.write("---")


    
    # import folium
    # from streamlit_folium import st_folium
    # import numpy as np

    st.subheader("🌍 Регіональні лідери платформ")
    st.write("Яка платформа домінує на кожному континенті?")

    # 1. Словник логотипів (надійні посилання)
    platform_logos = {
        "Instagram": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg",
        "TikTok": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg",
        "Facebook": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg"
    }

    # Координати центрів (підправлені для кращого вигляду)
    region_coords = {
        "Europe": [50, 15],
        "Asia": [35, 90],
        "North America": [45, -100],
        "South America": [-15, -60],
        "Oceania": [-25, 135],
        "Africa": [5, 20]
    }

    # 2. Дані
    region_counts = df.groupby(['Region', 'Most_Used_Platform']).size().reset_index(name='Count')
    top_reg = region_counts.loc[region_counts.groupby('Region')['Count'].idxmax()]

    # 3. Створення карти (без тексту, (PositronNoLabels))
    m = folium.Map(
        location=[20, 0], 
        zoom_start=2, 
        tiles='https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    )

    for _, row in top_reg.iterrows():
        region = row['Region']
        count = row['Count']
        platform = row['Most_Used_Platform']
        
        if region in region_coords:
            # ФОРМУЛА РОЗМІРУ:
            # Базовий розмір 45px + приріст на основі кореня від кількості
            # Це зробить малі значення (як у Пд. Америці) помітними
            icon_size = 40 + (np.sqrt(count) * 4) 
            
            logo_url = platform_logos.get(platform, "")
            
            if logo_url:
                icon = folium.CustomIcon(logo_url, icon_size=(icon_size, icon_size))
                
                # Додаємо маркер
                folium.Marker(
                    location=region_coords[region],
                    icon=icon,
                    tooltip=f"<b>{region}</b><br>Платформа: {platform}<br>Кількість: {count}"
                ).add_to(m)

    # Відображення
    st_folium(m, width="100%", height=550)
    st.info("**Географічний розподіл:** Instagram домінує в більшості регіонів, тоді як TikTok та Facebook утримують лідерство в Південній Америці та Африці відповідно.")

    st.write("---")
    








    
    st.subheader('🗂️ Матриця концентрації')
    st.write('Де зосереджені користувачі кожної окремої мережі?')

    # 1. Готуємо дані (агрегуємо кількість)
    bubble_data = df.groupby(['Region', 'Most_Used_Platform']).size().reset_index(name='User_Count')

    # --- НОВИЙ БЛОК: Сортування категорій ---
    # Створюємо відсортовані списки назв
    sorted_platforms = sorted(bubble_data['Most_Used_Platform'].unique())
    sorted_regions = sorted(bubble_data['Region'].unique())
    # ----------------------------------------
    
    # 2. Будуємо категоріальний Bubble Chart
    fig_bubble = px.scatter(
        bubble_data,
        x="Region",
        y="Most_Used_Platform",
        size="User_Count",          # Розмір залежить від кількості
        color="User_Count",         # Колір для додаткового акценту
        text="User_Count",          # Виводимо число всередині або поруч
        size_max=60,                # Максимальний розмір бульбашки
        labels={
            "Region": "Регіон світу", 
            "Most_Used_Platform": "Соціальна мережа",
            "User_Count": "Кількість"
        },
        # ПРИМУСОВЕ СОРТУВАННЯ ТУТ:
        category_orders={
            "Most_Used_Platform": sorted_platforms,
            "Region": sorted_regions
        },
        color_continuous_scale="Viridis",
        height=600
    )

    # Налаштування вигляду
    fig_bubble.update_traces(textposition='middle center', textfont=dict(color='white'))
    fig_bubble.update_layout(
        xaxis={'side': 'top'}, # Переносимо назви регіонів вгору для зручності
        showlegend=False
    )

    st.plotly_chart(fig_bubble, use_container_width=True)

    
    st.info("""
    **Географічний інсайт:**
    * **Європейський хаб:** Європа є центром активності для більшості західних платформ.
    * **Азійська специфіка:** Тільки в Азії ми бачимо активність у WeChat, LINE та KakaoTalk.
    * **Глобальність Instagram:** Рядок Instagram має найяскравіші кольори майже в усіх стовпчиках.
    """)
    


    
   




elif page == "ML Діагностика":
    st.title("💻⚙️ Машинне навчання: Цифровий профіль")
    st.write("""
    Цей інструмент використовує логіку алгоритму **K-Means**, щоб визначити, до якої групи користувачів 
    ви належите, на основі ваших відповідей.
    """)

    st.subheader("Введіть ваші показники:")
    
    with st.container(border=True):
        col_in1, col_in2 = st.columns(2)
        
        with col_in1:
            usage = st.slider("Скільки годин на день ви проводите в соцмережах?", 0.0, 24.0, 5.0, step=0.25)
            sleep = st.slider("Скільки годин ви зазвичай спите?", 0.0, 12.0, 8.0, step=0.25)
        
        with col_in2:
            mental = st.select_slider("Оцініть свій ментальний стан (1 - погано, 10 - чудово)", options=list(range(1, 11)), value=8)
            performance = st.radio("Чи впливають соцмережі на вашу успішність?", ["Негативно", "Нейтрально/Позитивно"])

    # Кнопка для розрахунку
    if st.button("Визначити мій профіль", type="primary", width='stretch'):
        
        # ПЕРЕВІРКА РЕАЛЬНОСТІ ДАНИХ (Логічний фільтр)
        if (usage + sleep) > 24.0:
            st.error(f"⚠️ **Помилка даних:** Сума годин у мережі ({usage}) та сну ({sleep}) складає {usage + sleep} год. В добі всього 24 години. Будь ласка, скоригуйте введені дані.")
        else:
            # РОЗРАХУНОК (тільки якщо дані пройшли перевірку)
            risk_score = (usage * 0.4) + ((10 - mental) * 0.3) + ((8 - sleep) * 0.3)
            
            st.write("---")
            st.subheader("Результат аналізу:")
            
            if usage >= 6.0 or risk_score > 5.0:
                st.error("🔴 **Ваш профіль: Високий рівень залежності**")
                st.warning("Ваші показники збігаються з групою 'High Addiction'. Рекомендуємо переглянути цифрові звички.")
            elif usage >= 4.0 or risk_score > 3.0:
                st.warning("🟡 **Ваш профіль: Середній рівень (Група ризику)**")
                st.info("Ви знаходитесь у зоні 'Medium Addiction'.")
            else:
                st.success("🟢 **Ваш профіль: Збалансований користувач**")
                st.balloons()
                st.write("Ваші показники відповідають групі 'Low Addiction'.")



elif page == "Аналітичний звіт"
    try:
            # Відкриваємо та читаємо файл
            with open("STORYTELLING.md", "r", encoding="utf-8") as f:
                story_content = f.read()
            
            # Відображаємо вміст
            # unsafe_allow_html=True потрібен, якщо у вашому MD є HTML-теги (наприклад, для центрування картинок)
            st.markdown(story_content, unsafe_allow_html=True)
            
        except FileNotFoundError:
            st.error("Файл STORYTELLING.md не знайдено. Переконайтеся, що він лежить у корені проекту.")
