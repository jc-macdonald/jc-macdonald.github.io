// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "About",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-research-figures",
          title: "Research figures",
          description: "Computed examples, method diagrams and editable sources for research figures.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/figures/";
          },
        },{id: "nav-news",
          title: "news",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/news/";
          },
        },{id: "nav-computed-software-examples",
          title: "Computed software examples",
          description: "Spatial fields, stochastic simulations, replicated comparisons and incomplete-data reconstruction using released packages.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/software-examples/";
          },
        },{id: "nav-publications",
          title: "Publications",
          description: "Journal articles, preprints and manuscripts in preparation, with citation details and source links.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-research-and-software",
          title: "Research and software",
          description: "Models and software for studying changing systems, learning from incomplete data, and comparing interventions and research designs.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-modeling-in-practice",
          title: "Modeling in practice",
          description: "My contributions to infectious disease scenario projections, vaccination studies and the software used to run them.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/operational-modeling/";
          },
        },{id: "nav-repositories",
          title: "repositories",
          description: "GitHub repositories for research software and collaborative infrastructure.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/repositories/";
          },
        },{id: "nav-teaching",
          title: "Teaching",
          description: "Teaching, workshop facilitation, and instructional experience.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "nav-talks",
          title: "Talks",
          description: "Invited seminars, conference presentations, and symposia.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/talks/";
          },
        },{id: "nav-outside-work",
          title: "Outside work",
          description: "I love to travel, get outside, and move.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/extracurricular/";
          },
        },{id: "news-announcement-3",
          title: "Plankton dynamics at SMB 2025",
          description: "",
          section: "News",
            handler: () => {
              window.location.href = "/news/announcement_3/";
            },
        },{id: "news-announcement-2",
          title: "Decision-Support Modeling seminar at UMBC",
          description: "",
          section: "News",
            handler: () => {
              window.location.href = "/news/announcement_2/";
            },
        },{id: "news-announcement-1",
          title: "Cross-Scale Feedback Motifs at Woods Hole",
          description: "",
          section: "News",
            handler: () => {
              window.location.href = "/news/announcement_1/";
            },
        },{id: "news-announcement-4",
          title: "FlepiMoP2 tools workshop at Insight Net",
          description: "",
          section: "News",
            handler: () => {
              window.location.href = "/news/announcement_4/";
            },
        },{id: "news-announcement-5",
          title: "One Health modeling at SMB 2026",
          description: "",
          section: "News",
            handler: () => {
              window.location.href = "/news/announcement_5/";
            },
        },{id: "projects-current-analyses",
          title: "Research in progress",
          description: "Ongoing work on structural scores, scientific machine learning and disease-modeling applications.",
          section: "Projects",
            handler: () => {
              window.location.href = "/projects/current_analyses/";
            },
        },{id: "projects-flepimop2",
          title: "FlepiMoP2",
          description: "Coordinate simulation runs across locations and scenarios, with reusable models and data tools.",
          section: "Projects",
            handler: () => {
              window.location.href = "/projects/flepimop2/";
            },
        },{id: "projects-inference-calibration",
          title: "op_infer",
          description: "Estimate model quantities from incomplete data and assess fitting methods. Private pre-alpha research software.",
          section: "Projects",
            handler: () => {
              window.location.href = "/projects/inference_calibration/";
            },
        },{id: "projects-op-engine",
          title: "OP Engine",
          description: "Simulate changing systems and random events, from spatial dynamics to population counts.",
          section: "Projects",
            handler: () => {
              window.location.href = "/projects/op_engine/";
            },
        },{id: "projects-op-system",
          title: "OP System",
          description: "Describe models of changing systems, including spatial interactions and random events.",
          section: "Projects",
            handler: () => {
              window.location.href = "/projects/op_system/";
            },
        },{id: "projects-pp-eigentest",
          title: "pp-eigentest",
          description: "Research on distinguishing underlying patterns from noise in incomplete data. Private alpha research software.",
          section: "Projects",
            handler: () => {
              window.location.href = "/projects/pp_eigentest/";
            },
        },{id: "projects-trade-study",
          title: "trade-study",
          description: "Compare experiments and model choices, weighing uncertainty, information and cost.",
          section: "Projects",
            handler: () => {
              window.location.href = "/projects/trade_study/";
            },
        },{id: "projects-vbpca-py",
          title: "vbpca-py",
          description: "Find shared patterns in incomplete datasets and assess uncertainty in those summaries.",
          section: "Projects",
            handler: () => {
              window.location.href = "/projects/vbpca_py/";
            },
        },{
        id: 'social-cv',
        title: 'Download CV (PDF)',
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
        id: 'social-wos',
        title: 'Web of Science',
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
