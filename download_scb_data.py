import requests
import pandas as pd

def fetch_scb_data(url, name, filename, query, aggregate):

    r = requests.post(url, json=query)
    r.raise_for_status()
    data = r.json()["data"]

    df = pd.DataFrame([
        {"date": d["key"][-1], name: float(d["values"][0])}
        for d in data
    ])

    if aggregate: # Summera om samma månad förekommer flera gånger
        df = (
            df
            .groupby("date", as_index=False)
            .sum()
            .rename(columns={"value": name})
        )

    df = df.iloc[::-1].reset_index(drop=True)

    df.to_csv(f"raw_data/{filename}", index=False)
    print(f"Saved {filename}")

# All metrics and their query
metrics = [
    {
        "name": "kpi",
        "url": "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/PR/PR0101/PR0101A/KPItotM",
        "filename": "kpi.csv",
        "query": {
            "query": [
                {
                    "code": "ContentsCode",
                    "selection": {
                        "filter": "item",
                        "values": ["000004VU"]
                    }
                },
                {
                    "code": "Tid",
                    "selection": {
                        "filter": "all",
                        "values": ["*"]
                    }
                }
            ],
            "response": {
                "format": "JSON"
            }
        },
        "aggregate": False
    },

    {
        "name": "statsskuld",
        "url": "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/OE/OE0202/OE0202A/StatsskuldNy",
        "filename": "statsskuld.csv",
        "query": {
            "query": [
                {
                    "code": "Marknad",
                    "selection": {
                        "filter": "item",
                        "values": ["SSTot"]
                    }
                },
                {
                    "code": "Tid",
                    "selection": {
                        "filter": "all",
                        "values": ["*"]
                    }
                }
            ],
            "response": {
                "format": "JSON"
            }
        },
        "aggregate": False
    },

    {
        "name": "arbetsloshet",
        "url": "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/AM/AM0401/AM0401A/AKURLBefM",
        "filename": "arbetsloshet.csv",
        "query": {
            "query": [
                {
                    "code": "Arbetskraftstillh",
                    "selection": {
                        "filter": "item",
                        "values": ["ALÖSP"]
                    }
                },
                {
                    "code": "TypData",
                    "selection": {
                        "filter": "agg:ISD2",
                        "values": ["O_DATA"]
                    }
                },
                {
                    "code": "Kon",
                    "selection": {
                        "filter": "item",
                        "values": ["1+2"]
                    }
                },
                {
                    "code": "Alder",
                    "selection": {
                        "filter": "item",
                        "values": ["tot15-74"]
                    }
                },
                {
                    "code": "Tid",
                    "selection": {
                        "filter": "all",
                        "values": ["*"]
                    }
                }
            ],
            "response": {
                "format": "JSON"
            }
        },
        "aggregate": False
    },

    {
        "name": "penningmangd",
        "url": "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/FM/FM5001/FM5001A/FM5001penningmangd",
        "filename": "penningmangd.csv",
        "query": {
            "query": [
                {
                    "code": "Penningm",
                    "selection": {
                        "filter": "item",
                        "values": ["5LLM1.1E.NEP.V.A"]
                    }
                },
                {
                    "code": "ContentsCode",
                    "selection": {
                        "filter": "item",
                        "values": ["000007WT"]
                    }
                }
            ],
            "response": {
                "format": "JSON"
            }
        },
        "aggregate": False
    },

    {
        "name": "bolaneranta",
        "url": "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/FM/FM5001/FM5001X/NTFM5001",
        "filename": "bolaneranta.csv",
        "query": {
            "query": [
                {
                    "code": "NyckeltalSCB",
                    "selection": {
                        "filter": "item",
                        "values": ["FMS03"]
                    }
                },
                {
                    "code": "ContentsCode",
                    "selection": {
                        "filter": "item",
                        "values": ["000000UW"]
                    }
                }
            ],
            "response": {
                "format": "JSON"
            }
        },
        "aggregate": False
    },

    {
        "name": "elanvandning",
        "url": "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/EN/EN0108/EN0108A/ElanvM",
        "filename": "elanvandning.csv",
        "query": {
            "query": [
                {
                    "code": "AnvOmrade",
                    "selection": {
                        "filter": "item",
                        "values": ["Tot"]
                    }
                },
                {
                    "code": "Tid",
                    "selection": {
                        "filter": "all",
                        "values": ["*"]
                    }
                }
            ],
            "response": {
                "format": "JSON"
            }
        },
        "aggregate": False
    },

    {
        "name": "befolkning1",
        "url": "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101A/BefolkManadCKM",
        "filename": "befolkning1.csv",
        "query": {
  "query": [
    {
      "code": "Region",
      "selection": {
        "filter": "vs:CKM01Riket",
        "values": [
          "00"
        ]
      }
    },
    {
      "code": "Alder",
      "selection": {
        "filter": "vs:CKM01AlderTot",
        "values": [
          "TotSA"
        ]
      }
    },
    {
      "code": "Kon",
      "selection": {
        "filter": "item",
        "values": [
          "TotSa"
        ]
      }
    }
  ],
  "response": {
    "format": "JSON"
  }
},
"aggregate": False
    },

    {
        "name": "befolkning2",
        "url": "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101A/BefolkManad",
        "filename": "befolkning2.csv",
        "query": {
  "query": [
    {
      "code": "Region",
      "selection": {
        "filter": "vs:HelaRiket",
        "values": [
          "00"
        ]
      }
    },
    {
      "code": "Alder",
      "selection": {
        "filter": "agg:Ålder10årJ",
        "values": [
          "-9",
          "10-19",
          "20-29",
          "30-39",
          "40-49",
          "50-59",
          "60-69",
          "70-79",
          "80-89",
          "90-99",
          "100+"
        ]
      }
    },
    {
      "code": "Kon",
      "selection": {
        "filter": "item",
        "values": [
          "1",
          "2"
        ]
      }
    }
  ],
  "response": {
    "format": "JSON"
  }
},
"aggregate": True
    }

]

for metric in metrics:
    fetch_scb_data(
        url=metric["url"],
        name=metric["name"],
        filename=metric["filename"],
        query=metric["query"],
        aggregate= metric["aggregate"]
    )

# KPI - fastställda tal
# Statsskuld - total alla markander
# Arbetslöshet AKU - procent, Icke säsongrensad, Total män och kvinnor, Totalt 15-74 år	
# Pänningmängd - Tillväxttakt 12-månaders, procent efter penningmängdsmått och månad
# Bolåneränta (nyckeltal) - genomsnitt, procentssats
# Elanvändning - summa förburkad el
# Befolkning1 - totalt år 2025
# Befolkning2 - totalt år 2000-2024
