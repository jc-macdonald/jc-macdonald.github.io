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
          description: "Research software for scientific computing, Bayesian inference, and operational deployment infrastructure.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-operational-deployments",
          title: "operational deployments",
          description: "Operational infectious disease forecasting and scenario modeling deployed through ACCIDDA&#39;s computational infrastructure.",
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
          description: "Teaching, workshop facilitation, and instructional experience.",
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
        },{id: "news-presenting-at-smb-2025-in-edmonton-recovering-ecological-geometry-a-trait-and-depth-structured-ipde-model-of-plankton-dynamics",
          title: 'Presenting at SMB 2025 in Edmonton — “Recovering Ecological Geometry: A Trait- and...',
          description: "",
          section: "News",},{id: "news-invited-seminar-at-umbc-decision-support-modeling-for-one-health-pathogens",
          title: 'Invited seminar at UMBC — “Decision-Support Modeling for One Health Pathogens.”',
          description: "",
          section: "News",},{id: "news-invited-seminar-at-woods-hole-oceanographic-institution-cross-scale-feedback-motifs-structure-preserving-models-and-computational-tools-for-complex-systems",
          title: 'Invited seminar at Woods Hole Oceanographic Institution — “Cross-Scale Feedback Motifs: Structure-Preserving Models...',
          description: "",
          section: "News",},{id: "news-presenting-flepimop2-and-the-operator-partitioned-simulation-stack-at-the-insight-net-third-annual-meeting-tools-workshop-friday-center-chapel-hill-nc",
          title: 'Presenting FlepiMoP2 and the Operator-Partitioned Simulation Stack at the Insight Net Third Annual...',
          description: "",
          section: "News",},{id: "news-mini-symposium-talk-at-smb-2026-in-graz-austria-decision-support-modeling-for-one-health-pathogens-using-mechanistic-models-for-surveillance-and-forecast-design",
          title: 'Mini-symposium talk at SMB 2026 in Graz, Austria — “Decision-Support Modeling for One...',
          description: "",
          section: "News",},{id: "projects-flepimop2",
          title: 'FlepiMoP2',
          description: "Configuration-driven orchestration engine for CDC-supported infectious disease forecasting and scenario analysis. Plugin architecture decoupling model specification, integration, and persistence.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/flepimop2/";
            },},{id: "projects-op-engine",
          title: 'OP Engine',
          description: "Operator-partitioned ODE/PDE solver core with nine integration methods (explicit, IMEX, fully implicit), adaptive step-size control, and zero per-step allocation.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/op_engine/";
            },},{id: "projects-op-system",
          title: 'OP System',
          description: "Declarative specification language and compiler for structured dynamical systems. Two specification pathways, multi-axis stratification, and compilation to validated bytecode closures.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/op_system/";
            },},{id: "projects-pp-eigentest",
          title: 'pp-eigentest',
          description: "Posterior predictive eigenvalue testing for signal rank determination. Three-layer consensus architecture with FWER and FDR control; NumPy and JAX backends.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/pp_eigentest/";
            },},{id: "projects-trade-study",
          title: 'trade-study',
          description: "Design and evaluation framework for scientific simulation studies. Score competing configurations — model formulations, solver choices, measurement strategies, or any design decision — against known ground truth via protocol-driven simulators, proper scoring rules, hierarchical phases, multi-objective Pareto optimization, and Bayesian model stacking.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/trade_study/";
            },},{id: "projects-vbpca-py",
          title: 'vbpca-py',
          description: "Variational Bayesian PCA for incomplete data with full posterior uncertainty, automatic component pruning, native missingness handling, and C++-accelerated kernels.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/vbpca_py/";
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
