import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="To terningar – simulering", page_icon="🎲")
st.title("Simulering av to terningar 🎲🎲")

# --- Inndata ---
antall_kast = st.number_input("Velg antal kast", min_value=1, value=1000, step=100)
kolonner = st.columns(2)
with kolonner[0]:
    vis_teori = st.checkbox("Vis teoretisk fordeling", value=True)
with kolonner[1]:
    fast_seed = st.checkbox("Bruk fast tilfeldighetsfrø (gjør resultatet repeterbart)", value=False)

# --- Kjør simulering ---
if st.button("Kast terningane!"):
    if fast_seed:
        np.random.seed(42)

    # To uavhengige terningar, summering gir verdiar 2..12
    t1 = np.random.randint(1, 7, size=antall_kast)
    t2 = np.random.randint(1, 7, size=antall_kast)
    summer = t1 + t2

    # Frekvens og relativ frekvens per sum
    verdier, counts = np.unique(summer, return_counts=True)
    df = pd.DataFrame({"sum": verdier, "frekvens": counts})
    df = df.set_index("sum").reindex(range(2, 13), fill_value=0)  # sørg for alle 2..12 finnes
    df["andel"] = df["frekvens"] / antall_kast

    st.subheader("Søylediagram (frekvens)")
    st.bar_chart(df["frekvens"], height=300)

    st.caption("Tips: Hold musepeikaren over søylene for nøyaktige verdiar.")
    st.write(f"Totalt {antall_kast} kast.")

    if vis_teori:
        # Teoretiske sannsyn for summen av to terningar
        # Antall gunstige for kvar sum (2..12): 1,2,3,4,5,6,5,4,3,2,1 av totalt 36
        gunstige = np.array([1,2,3,4,5,6,5,4,3,2,1], dtype=float)
        teori = pd.DataFrame(
            {
                "sum": np.arange(2, 13),
                "teoretisk_andel": gunstige / 36,
                "forventa_frekvens": (gunstige / 36) * antall_kast,
            }
        ).set_index("sum")

        st.subheader("Samanlikning: simulert vs. teoretisk")
        sam = df.join(teori)
        st.dataframe(
            sam[["frekvens", "forventa_frekvens", "andel", "teoretisk_andel"]]
            .round(4)
            .rename(
                columns={
                    "frekvens": "Simulert frekvens",
                    "forventa_frekvens": "Forventa (teori)",
                    "andel": "Simulert andel",
                    "teoretisk_andel": "Teoretisk andel",
                }
            ),
            use_container_width=True,
        )

        st.subheader("Søylediagram (simulert vs. forventa frekvens)")
        plotdf = sam[["frekvens", "forventa_frekvens"]].rename(
            columns={"frekvens": "Simulert", "forventa_frekvens": "Teori"}
        )
        st.bar_chart(plotdf, height=320)
