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
  },{id: "nav-proyectos",
          title: "Proyectos",
          description: "Proyectos de análisis de datos, modelamiento y evaluación económica.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-projects",
          title: "Projects",
          description: "Data analysis, modelling and economic appraisal projects.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/en/projects/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "Currículum Vitae de Vicente Lombardozzi — Research Analyst, economía y datos.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "Curriculum Vitae of Vicente Lombardozzi — Research Analyst, economics and data.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/en/cv/";
          },
        },{id: "projects-descomposición-del-crecimiento-y-regresiones-log-log",
          title: 'Descomposición del crecimiento y regresiones log-log',
          description: "Identidad de Kaya para Chile (1990-2013), regresiones log-log entre 90 países y proyecciones de escenarios. MATLAB (2019) y Python (2026).",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_chile_co2/";
            },},{id: "projects-growth-decomposition-and-log-log-regressions",
          title: 'Growth Decomposition and Log-Log Regressions',
          description: "Kaya identity for Chile (1990-2013), cross-country log-log regressions (90 countries) and scenario projections. MATLAB (2019) and Python (2026).",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_chile_co2_en/";
            },},{id: "projects-dashboard-de-indicadores-macro-de-chile",
          title: 'Dashboard de indicadores macro de Chile',
          description: "Base de datos y dashboard interactivo de indicadores económicos de Chile (2000-2023) con datos públicos.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_powerbi_chile/";
            },},{id: "projects-chile-macro-indicators-dashboard",
          title: 'Chile Macro Indicators Dashboard',
          description: "Database and interactive dashboard of Chilean economic indicators (2000-2023) built from public data.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_powerbi_chile_en/";
            },},{id: "projects-modelos-dinámicos-de-stock-y-flujo",
          title: 'Modelos dinámicos de stock y flujo',
          description: "Reimplementación en Python (scipy) de modelos de dinámica de sistemas trabajados en Vensim durante el MSc.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_system_dynamics/";
            },},{id: "projects-stock-and-flow-dynamic-models",
          title: 'Stock-and-Flow Dynamic Models',
          description: "Python (scipy) re-implementation of system-dynamics models I worked on in Vensim during my MSc.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_system_dynamics_en/";
            },},{id: "projects-evaluación-de-un-proyecto-de-inversión-van-y-sensibilidad",
          title: 'Evaluación de un proyecto de inversión (VAN y sensibilidad)',
          description: "Análisis costo-beneficio a 20 años de un proyecto de infraestructura en un liceo de Valparaíso, con dos ofertas reales. Excel (2019) y Python (2026).",
          section: "Projects",handler: () => {
              window.location.href = "/projects/7_cba_solar/";
            },},{id: "projects-investment-appraisal-npv-and-sensitivity",
          title: 'Investment Appraisal (NPV and Sensitivity)',
          description: "20-year cost-benefit analysis of an infrastructure project at a Valparaíso high school, with two real bids. Excel (2019) and Python (2026).",
          section: "Projects",handler: () => {
              window.location.href = "/projects/7_cba_solar_en/";
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
