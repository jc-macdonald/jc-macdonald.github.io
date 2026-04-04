// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-publications",
          title: "publications",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-projects",
          title: "projects",
          description: "Research software for scientific computing, Bayesian inference, and operational modeling infrastructure.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-operational-modeling",
          title: "operational modeling",
          description: "Operational infectious disease forecasting and scenario modeling for CDC-CFA and the Scenario Modeling Hubs.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/operational-modeling/";
          },
        },{id: "nav-talks",
          title: "talks",
          description: "Invited seminars, conference presentations, and symposia.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/talks/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-teaching",
          title: "teaching",
          description: "Teaching and instructional experience.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "nav-extracurricular",
          title: "extracurricular",
          description: "I love to travel, get outside, and move.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/extracurricular/";
          },
        },{id: "books-the-godfather",
          title: 'The Godfather',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/the_godfather/";
            },},{id: "news-presenting-at-smb-2025-in-edmonton-recovering-ecological-geometry-a-trait-and-depth-structured-ipde-model-of-plankton-dynamics",
          title: 'Presenting at SMB 2025 in Edmonton — “Recovering Ecological Geometry: A Trait- and...',
          description: "",
          section: "News",},{id: "news-invited-seminar-at-umbc-decision-support-modeling-for-one-health-pathogens",
          title: 'Invited seminar at UMBC — “Decision-Support Modeling for One Health Pathogens.”',
          description: "",
          section: "News",},{id: "news-invited-seminar-at-woods-hole-oceanographic-institution-cross-scale-feedback-motifs-structure-preserving-models-and-computational-tools-for-complex-systems",
          title: 'Invited seminar at Woods Hole Oceanographic Institution — “Cross-Scale Feedback Motifs: Structure-Preserving Models...',
          description: "",
          section: "News",},{id: "projects-flepimop2",
          title: 'FlepiMoP2',
          description: "Modular epidemic modeling and simulation pipeline for forecasting and scenario analysis. Core contributor to the redesign of ACCIDDA&#39;s operational infrastructure.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/flepimop2/";
            },},{id: "projects-model-criticism",
          title: 'model-criticism',
          description: "Observable-based model evaluation with Pareto optimization, proper scoring rules, and Bayesian stacking for simulation studies.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/model_criticism/";
            },},{id: "projects-op-engine",
          title: 'OP Engine',
          description: "Numerical simulation engine for mechanistic models of biological and epidemiological systems. Supports ODE, PDE, and hybrid operator-splitting solvers with pluggable backends.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/op_engine/";
            },},{id: "projects-op-system",
          title: 'OP System',
          description: "Declarative governing equation specification compiler for structured dynamical systems. Transforms YAML model definitions into callable numerics.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/op_system/";
            },},{id: "projects-pp-eigentest",
          title: 'pp-eigentest',
          description: "Posterior predictive eigenvalue testing for determining signal rank in covariance and Gram matrices. Supports ordered hypothesis testing with FWER and FDR control.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/pp_eigentest/";
            },},{id: "projects-vbpca-py",
          title: 'vbpca-py',
          description: "Variational Bayesian PCA for incomplete data with native missing-data handling, uncertainty quantification, and C++-accelerated kernels. scikit-learn compatible.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/vbpca_py/";
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
        id: 'social-cv',
        title: 'CV',
        section: 'Socials',
        handler: () => {
          window.open("/assets/pdf/cv.pdf", "_blank");
        },
      },{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%6A%6D%61%63%64%6F%31%36@%6A%68.%65%64%75", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/jc-macdonald", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=VxTPRq8AAAAJ", "_blank");
        },
      },{
        id: 'social-orcid',
        title: 'ORCID',
        section: 'Socials',
        handler: () => {
          window.open("https://orcid.org/0000-0002-3643-6266", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/j-caleb-macdonald-674840a2", "_blank");
        },
      },{
        id: 'social-researchgate',
        title: 'ResearchGate',
        section: 'Socials',
        handler: () => {
          window.open("https://www.researchgate.net/profile/Joshua_Macdonald4/", "_blank");
        },
      },{
        id: 'social-wos_id',
        title: 'Wos_id',
        section: 'Socials',
        handler: () => {
          window.open("https://www.webofscience.com/wos/author/record/IWE-2826-2023", "_blank");
        },
      },{
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
