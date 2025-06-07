import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def mostrar_comparativas(jug1, jug2, df):
    df_sel = df[df["Player"].isin([jug1, jug2])].set_index("Player")
    colors = ['#1f77b4', '#ff7f0e']

    # Expander: Comparación Servicio
    with st.expander("Al Servicio"):
        variables = ['2ndAgg', '2nd: Unret%']
        labels_mostrar = ['Agresividad 2º Servicio', '% Saques No Devueltos con 2º servicio']

        for var, label in zip(variables, labels_mostrar):
            x = np.arange(2)
            fig, ax = plt.subplots(figsize=(5, 3.5))
            for i, jugador in enumerate([jug1, jug2]):
                valor = df_sel.loc[jugador, var]
                ax.bar(i, valor, color=colors[i], label=jugador)
            ax.set_xticks(x)
            ax.set_xticklabels([jug1, jug2])
            ax.set_ylabel("Valor")
            ax.set_title(label)
            ax.legend(loc="lower right", prop={'size': 8})
            st.pyplot(fig)

# Gráfico 2: Dirección del saque "Wide" (usando jug1 y jug2)
        variables_wide = ['D Wide%', 'A Wide%']
        labels_wide = ['Dirección Wide (Deuce)', 'Dirección Wide (Ad)']

        if all(v in df.columns for v in variables_wide):
            x = np.arange(len(variables_wide))
            width = 0.35
            fig, ax = plt.subplots(figsize=(6, 4))

            for i, jugador in enumerate([jug1, jug2]):
                valores = df_sel.loc[jugador, variables_wide].values
                ax.bar(x + i * width - width / 2, valores, width, label=jugador)

            ax.set_xticks(x)
            ax.set_xticklabels(labels_wide)
            ax.set_ylabel("Porcentaje (%)")
            ax.set_title("Dirección del saque: Wide en Deuce y Ad")
            ax.legend(loc="lower right", prop={'size': 8})
            ax.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig)
        else:
            st.warning("Faltan columnas para mostrar la dirección del saque.")

    # Expander: Comparación Rallys
    with st.expander("En Rallys"):
        # Gráfica 1: Duración media del rally
        variables_rally = ['RLen-Serve', 'RLen-Return']
        labels_rally = ['Rally medio al saque', 'Rally medio al resto']
        x = np.arange(len(variables_rally))
        width = 0.35
        fig, ax = plt.subplots(figsize=(6, 4))
        for i, jugador in enumerate([jug1, jug2]):
            valores = df_sel.loc[jugador, variables_rally].values
            ax.bar(x + i * width - width / 2, valores, width, label=jugador)
        ax.set_xticks(x)
        ax.set_xticklabels(labels_rally)
        ax.set_ylabel("Duración media (golpes)")
        ax.set_title("Duración media del rally")
        ax.legend(loc="lower right", prop={'size': 8})
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)

        # Gráfica 2: Radar de rallies ganados
        labels_radar = ['1-3 W%', '4-6 W%', '7-9 W%', '10+ W%']
        df_filtrado = df[df['Player'].isin([jug1, jug2])].copy()
        angles = np.linspace(0, 2 * np.pi, len(labels_radar), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        def add_player(ax, row, label):
            values = [row[var] for var in labels_radar] + [row[labels_radar[0]]]
            ax.plot(angles, values, label=label)
            ax.fill(angles, values, alpha=0.25)

        for _, row in df_filtrado.iterrows():
            add_player(ax, row, row['Player'])

        valores_min = df_filtrado[labels_radar].min().min()
        valores_max = df_filtrado[labels_radar].max().max()
        margen = (valores_max - valores_min) * 0.1
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels_radar)
        ax.set_ylim(valores_min - margen, valores_max + margen)
        ax.set_title("Rallies ganados por duración")
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        st.pyplot(fig)

     # Expander: Comparación Táctica
    with st.expander("Variación de Táctica"):
        metricas = ['SnV Freq', 'Drop: Freq']

        if all(m in df.columns for m in metricas):
            df_sel_tac = df[df['Player'].isin([jug1, jug2])].set_index('Player')

            x = np.arange(len(metricas))
            width = 0.35

            fig, ax = plt.subplots(figsize=(6, 5))

            val1 = df_sel_tac.loc[jug1, metricas]
            val2 = df_sel_tac.loc[jug2, metricas]

            ax.bar(x - width/2, val1, width, label=jug1)
            ax.bar(x + width/2, val2, width, label=jug2)

            ax.set_xticks(x)
            ax.set_xticklabels(['Serve & Volley (%)', 'Dropshot Frequency (%)'])
            ax.set_ylabel("Frecuencia (%)")
            ax.set_title("Comparación de variedad táctica: SnV vs Dejada")
            ax.legend(loc='upper right', prop={'size': 8})
            ax.grid(True, linestyle="--", alpha=0.3)

            st.pyplot(fig)
        else:
            st.warning("Faltan columnas para la comparación táctica.")

    # Expander: Juegos y Puntos Clave
    with st.expander("Juegos y Puntos Clave"):
        df_filtrado = df[df['Player'].isin([jug1, jug2])].copy()

        # Radar Chart: SvForSet, SvStaySet, SvForMatch, SvStayMatch
        labels_radar = ['SvForSet', 'SvStaySet', 'SvForMatch', 'SvStayMatch']
        if all(label in df.columns for label in labels_radar):
            angles = np.linspace(0, 2 * np.pi, len(labels_radar), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

            def add_player(ax, row, label):
                values = [row[var] for var in labels_radar]
                values += values[:1]
                ax.plot(angles, values, label=label)
                ax.fill(angles, values, alpha=0.25)

            for _, row in df_filtrado.iterrows():
                add_player(ax, row, row['Player'])

            valores_min = df_filtrado[labels_radar].min().min()
            valores_max = df_filtrado[labels_radar].max().max()
            margen = (valores_max - valores_min) * 0.1

            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            ax.set_thetagrids(np.degrees(angles[:-1]), labels_radar)
            ax.set_title("Comparación de desempeño en juegos clave")
            ax.set_ylim(valores_min - margen, valores_max + margen)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            st.pyplot(fig)
        else:
            st.warning("Faltan columnas para el radar de juegos clave.")

        # Gráfico de barras: BreakBack% y Consol%
        metricas_clave = ['BreakBack%', 'Consol%']
        if all(m in df.columns for m in metricas_clave):
            df_sel_clave = df[df['Player'].isin([jug1, jug2])].set_index('Player')

            x = np.arange(len(metricas_clave))
            width = 0.35
            fig, ax = plt.subplots(figsize=(6, 5))

            val1 = df_sel_clave.loc[jug1, metricas_clave]
            val2 = df_sel_clave.loc[jug2, metricas_clave]

            ax.bar(x - width/2, val1, width, label=jug1)
            ax.bar(x + width/2, val2, width, label=jug2)

            ax.set_xticks(x)
            ax.set_xticklabels(['BreakBack%', 'Consol%'])
            ax.set_ylabel("Porcentaje (%)")
            ax.set_title("Comparación mental: recuperación vs consolidación")
            ax.legend(loc="lower right", prop={'size': 8})
            ax.grid(True, linestyle="--", alpha=0.3)

            st.pyplot(fig)
        else:
            st.warning("Faltan columnas para la comparación mental.")

    # Expander: Winners y Errores No Forzados
    with st.expander("Winners y Errores No Forzados"):
        df_filtrado = df[df['Player'].isin([jug1, jug2])].set_index('Player')

        grupos = [
            (['Wnr/Pt', 'UFE/Pt'], ['Winners por punto', 'Errores no forzados por punto']),
            (['vs Wnr/Pt', 'vs UFE/Pt'], ['Winners recibidos por punto', 'Errores forzados al rival por punto'])
        ]

        width = 0.35

        for vars_, labels in grupos:
            if all(v in df.columns for v in vars_):
                x = np.arange(len(vars_))
                fig, ax = plt.subplots(figsize=(6, 4))

                for i, jugador in enumerate([jug1, jug2]):
                    valores = df_filtrado.loc[jugador, vars_].values
                    ax.bar(x + i * width - width / 2, valores, width, label=jugador)

                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=15)
                ax.set_ylabel("Valor")
                ax.set_title("Comparación táctica")
                ax.legend(loc="lower right", prop={'size': 8})
                ax.grid(True, linestyle='--', alpha=0.3)

                st.pyplot(fig)
            else:
                st.warning(f"Faltan columnas: {', '.join([v for v in vars_ if v not in df.columns])}")
                
