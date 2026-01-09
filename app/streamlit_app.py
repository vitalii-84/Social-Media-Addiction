import streamlit as st
import pandas as pd
import plotly.express as px

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
    ["Головна", "Аналіз гіпотез", "Глобальна географія", "ML Діагностика"]
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
        st.metric("Середній час в соцмережах", f"{df['Avg_Daily_Usage_Hours'].mean():.1f} год")
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
    tab1, tab2, tab3 = st.tabs(["🏥 Здоров'я та Психіка", "📱 Платформи", "🤝 Соціальні зв'язки"])
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


elif page == "Глобальна географія":
    st.title("🌍 Глобальна географія залежності")
    st.write("""
    На цьому етапі ми аналізуємо, як цифрова залежність розподілена по світу. 
    Дані були агреговані за макрорегіонами (континентами) для усунення статистичного шуму 
    від країн з поодинокими відповідями.
    """)

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


    
    st.subheader("🏆 Регіональні лідери платформ")
    st.write("Яка платформа домінує на кожному континенті?")

    # Готуємо дані (Варіант А з вашого аналізу)
    region_platform_counts = df.groupby(['Region', 'Most_Used_Platform']).size().reset_index(name='User_Count')
    top_platform_per_region = region_platform_counts.loc[region_platform_counts.groupby('Region')['User_Count'].idxmax()]
    
    # Створюємо колонки для карток (по 3 в ряд)
    rows = [st.columns(3), st.columns(3)]
    regions = top_platform_per_region.sort_values('User_Count', ascending=False).to_dict('records')

    for idx, reg in enumerate(regions):
        col = rows[idx // 3][idx % 3]
        with col:
            st.metric(label=f"📍 {reg['Region']}", value=reg['Most_Used_Platform'])
            st.caption(f"Користувачів: {reg['User_Count']}")

    st.write("---")
    
    
    
    
    st.write("---")
    st.subheader("🏆 Регіональні лідери платформ")
    st.write("Яка платформа домінує на кожному континенті?")

    # 1. Повний словник логотипів усіх платформ з датасету
    platform_icons = {
        "Instagram": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg",
        "TikTok": "https://upload.wikimedia.org/wikipedia/commons/a/a2/TikTok_Icon.svg", # Покращена іконка
        "Facebook": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg",
        "WhatsApp": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg",
        "YouTube": "https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg",
        "Twitter": "https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg", # Логотип X (Twitter)
        "LinkedIn": "https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg", # Покращена іконка
        "Snapchat": "https://upload.wikimedia.org/wikipedia/en/a/ad/Snapchat_logo.svg",
        "WeChat": "https://upload.wikimedia.org/wikipedia/commons/7/73/WeChat_logo.svg",
        "LINE": "https://upload.wikimedia.org/wikipedia/commons/4/41/LINE_logo.svg",
        "KakaoTalk": "https://upload.wikimedia.org/wikipedia/commons/e/e3/KakaoTalk_logo.svg",
        "VKontakte": "https://upload.wikimedia.org/wikipedia/commons/f/f3/VK_Logo.svg"
    }

    # 2. Підготовка даних
    region_counts = df.groupby(['Region', 'Most_Used_Platform']).size().reset_index(name='Count')
    top_platforms = region_counts.loc[region_counts.groupby('Region')['Count'].idxmax()]
    regions_list = top_platforms.sort_values('Count', ascending=False).to_dict('records')

    # 3. Створення сітки карток
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    all_cols = [col1, col2, col3, col4, col5, col6]

    for idx, reg in enumerate(regions_list):
        if idx < len(all_cols):
            with all_cols[idx]:
                with st.container(border=True):
                    # Назва регіону
                    st.markdown(f"### 📍 {reg['Region']}")
                    
                    # Логотип платформи
                    platform_name = reg['Most_Used_Platform']
                    logo_url = platform_icons.get(platform_name, "")
                    
                    if logo_url:
                        st.image(logo_url, width=45)
                    
                    # Назва та статистика
                    st.write(f"**{platform_name}**")
                    st.caption(f"Кількість відповідей: {reg['Count']}")

    st.write("---")



    st.write("---")
    st.subheader("🌍 Карта регіональних лідерів")
    st.write("Кольори відображають макрорегіони, а підписи — найпопулярнішу платформу.")

    # 1. Підготовка даних (Ваші результати Блоку 8)
    # Створюємо словник координат центрів для підписів
    region_centers = {
        "Europe": {"lat": 48, "lon": 15},
        "Asia": {"lat": 30, "lon": 100},
        "North America": {"lat": 45, "lon": -105},
        "South America": {"lat": -15, "lon": -60},
        "Africa": {"lat": 5, "lon": 20},
        "Oceania": {"lat": -25, "lon": 140}
    }

    # Знаходимо лідерів
    reg_counts = df.groupby(['Region', 'Most_Used_Platform']).size().reset_index(name='Count')
    top_reg = reg_counts.loc[reg_counts.groupby('Region')['Count'].idxmax()].copy()
    
    # Додаємо координати для відображення назв
    top_reg['lat'] = top_reg['Region'].map(lambda x: region_centers[x]['lat'])
    top_reg['lon'] = top_reg['Region'].map(lambda x: region_centers[x]['lon'])
    
    # Додаємо емодзі для візуалізації замість логотипів (це працює стабільно всюди)
    platform_emojis = {
        "Instagram": "📸 Instagram",
        "TikTok": "🎵 TikTok",
        "Facebook": "🔵 Facebook"
    }
    top_reg['Label'] = top_reg['Most_Used_Platform'].map(platform_emojis)

    # 2. Побудова карти
    # Основний шар - кольори регіонів
    fig_map = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Region",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        projection="natural earth",
        hover_data={"Country": True, "Region": False}
    )

    # Додаємо шар з підписами платформ
    fig_map.add_scattergeo(
        lat=top_reg['lat'],
        lon=top_reg['lon'],
        text=top_reg['Label'],
        mode='text',
        textfont=dict(size=14, color="black", family="Arial Black"),
        showlegend=False
    )

    fig_map.update_layout(
        height=600,
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(showcountries=True, countrycolor="white")
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.info("**Географічний розподіл:** Instagram домінує в більшості регіонів, тоді як TikTok та Facebook утримують лідерство в Південній Америці та Африці відповідно.")



    

    

    # Візуалізація "Ядро платформ" (Теплова карта)
    st.subheader("📊 Матриця популярності: Платформи vs Регіони")
    
    pivot_data = df.pivot_table(index='Most_Used_Platform', 
                                columns='Region', 
                                values='Student_ID', 
                                aggfunc='count', 
                                fill_value=0)

    fig_heat = px.imshow(
        pivot_data,
        labels=dict(x="Регіон", y="Платформа", color="Кількість"),
        x=pivot_data.columns,
        y=pivot_data.index,
        color_continuous_scale="Viridis",
        title="Де зосереджена аудиторія кожної мережі?"
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.info("**Географічний інсайт:** Європа виступає головним хабом для більшості мереж, тоді як Азія демонструє унікальність через високу популярність локальних месенджерів (WeChat, LINE, KakaoTalk).")





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
