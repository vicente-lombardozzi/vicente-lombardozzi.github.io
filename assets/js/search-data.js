// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-sobre-mí",
    title: "Sobre mí",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-publicaciones",
          title: "Publicaciones",
          description: "Artículos académicos, libro y tesis publicados, en orden cronológico inverso.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-proyectos",
          title: "Proyectos",
          description: "Portafolio de proyectos de análisis de datos, sostenibilidad e investigación aplicada.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "Currículum Vitae de Vicente Lombardozzi — Data Analyst &amp; Sustainability Researcher.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "books-the-godfather",
          title: 'The Godfather',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/the_godfather/";
            },},{id: "news-obtuve-el-grado-de-msc-in-ecological-economics-en-la-university-of-leeds-reino-unido-con-una-tesis-sobre-sostenibilidad-económica-de-ecoaldeas",
          title: '🎓 Obtuve el grado de MSc in Ecological Economics en la University of...',
          description: "",
          section: "News",},{id: "news-co-fundador-de-stratnova-un-emprendimiento-en-etapa-inicial-dedicado-a-soluciones-de-ia-conversacional-para-automatización-de-ventas",
          title: '🧠 Co-fundador de StratNova, un emprendimiento en etapa inicial dedicado a soluciones de...',
          description: "",
          section: "News",},{id: "news-portafolio-en-construcción-activa-desarrollando-siete-proyectos-de-data-analytics-aplicados-a-sostenibilidad-economía-ecológica-y-políticas-públicas-en-chile",
          title: '🚀 Portafolio en construcción activa. Desarrollando siete proyectos de data analytics aplicados a...',
          description: "",
          section: "News",},{id: "projects-emisiones-de-co2-en-chile",
          title: 'Emisiones de CO2 en Chile',
          description: "Re-analisis en Python de mi tesina del MSc Leeds 2019. KAYA, STIRPAT y proyecciones al 2050.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_chile_co2/";
            },},{id: "projects-dashboard-indicadores-chile",
          title: 'Dashboard Indicadores Chile',
          description: "Dashboard interactivo con datos del Banco Mundial y CASEN. Construido en Plotly como alternativa open-source equivalente a Power BI.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_powerbi_chile/";
            },},{id: "projects-desigualdad-de-ingresos-en-chile",
          title: 'Desigualdad de Ingresos en Chile',
          description: "Analisis estadistico en R de desigualdad economica y de tiempo en Chile, usando datos de CASEN y ENUT.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_desigualdad_r/";
            },},{id: "projects-sentiment-analysis-en-espanol",
          title: 'Sentiment Analysis en Espanol',
          description: "Comparacion de tres enfoques de NLP para clasificar sentimiento en resenas en espanol, desde un lexicon simple hasta TF-IDF y SVM.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_nlp_sentiment/";
            },},{id: "projects-base-de-datos-de-ecoaldeas-chilenas",
          title: 'Base de Datos de Ecoaldeas Chilenas',
          description: "Diseno e implementacion de una base de datos relacional PostgreSQL para gestionar informacion sobre comunidades ecologicas chilenas.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_ecoaldeas_sql/";
            },},{id: "projects-system-dynamics-de-vensim-a-python",
          title: 'System Dynamics de Vensim a Python',
          description: "Re-implementacion en Python (scipy.integrate) de modelos de dinamica de sistemas que originalmente construi en Vensim durante mi MSc en Leeds.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_system_dynamics/";
            },},{id: "projects-cba-paneles-solares-liceo",
          title: 'CBA Paneles Solares Liceo',
          description: "Re-implementacion en Python de un CBA real sobre instalacion de 70 kWp fotovoltaicos en el Liceo Alfredo Nazar Feres (Valparaiso).",
          section: "Projects",handler: () => {
              window.location.href = "/projects/7_cba_solar/";
            },},{id: "teachings-data-science-fundamentals",
          title: 'Data Science Fundamentals',
          description: "This course covers the foundational aspects of data science, including data collection, cleaning, analysis, and visualization. Students will learn practical skills for working with real-world datasets.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/data-science-fundamentals/";
            },},{id: "teachings-introduction-to-machine-learning",
          title: 'Introduction to Machine Learning',
          description: "This course provides an introduction to machine learning concepts, algorithms, and applications. Students will learn about supervised and unsupervised learning, model evaluation, and practical implementations.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/introduction-to-machine-learning/";
            },},{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
