import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Super Maths",
    page_icon="🧮",
    layout="centered"
)

# Fonction utilitaire pour le style
def show_header(title, emoji):
    st.markdown(f"## {emoji} {title}")
    st.markdown("---")

# --- 1. PROBABILITÉS ---
def page_probabilites():
    show_header("Probabilités", "🎲")
    
    tab1, tab2, tab3 = st.tabs(["Simple", "Combinatoire", "Binomiale"])
    
    with tab1:
        st.subheader("Probabilité Simple")
        col1, col2 = st.columns(2)
        total = col1.number_input("Cas possibles (Total)", min_value=1, value=10, step=1)
        favorables = col2.number_input("Cas favorables", min_value=0, value=2, step=1)
        
        if favorables > total:
            st.error("Erreur : Les cas favorables ne peuvent pas dépasser le total.")
        else:
            p = favorables / total
            st.success(f"**P(A) = {p:.4f}** ({p*100:.2f}%)")
            # Graphique simple (Barre de progression)
            st.progress(p)
    
    with tab2:
        st.subheader("Combinatoire")
        col1, col2 = st.columns(2)
        n = col1.number_input("n (total)", min_value=1, value=5, step=1)
        k = col2.number_input("k (choix)", min_value=0, value=2, step=1)
        
        if k > n:
            st.error("Erreur : k > n impossible.")
        else:
            res = math.comb(n, k)
            st.latex(f"C({n}, {k}) = \\binom{{{n}}}{{{k}}} = {res}")
            st.info(f"Soit **{res}** combinaisons possibles.")

    with tab3:
        st.subheader("Loi Binomiale")
        col1, col2 = st.columns(2)
        n_bio = col1.number_input("Nombre d'essais (n)", min_value=1, value=10, step=1)
        k_bio = col2.number_input("Nombre de succès (k)", min_value=0, value=5, step=1)
        p_bio = st.slider("Proba de succès (p)", 0.0, 1.0, 0.5, step=0.01)

        if k_bio > n_bio:
            st.error("k ne peut pas être supérieur à n.")
        else:
            prob = math.comb(n_bio, k_bio) * (p_bio ** k_bio) * ((1 - p_bio) ** (n_bio - k_bio))
            st.latex(f"P(X={k_bio}) = \\binom{{{n_bio}}}{{{k_bio}}} \\times {p_bio:.2f}^{{{k_bio}}} \\times (1-{p_bio:.2f})^{{{n_bio-k_bio}}}")
            st.success(f"**Probabilité = {prob:.4f}** ({prob*100:.2f}%)")

# --- 2. SUITES ARITHMÉTIQUES ---
def page_suites():
    show_header("Suites Arithmétiques", "📊")
    
    st.markdown("Entrez les premiers termes séparés par un espace.")
    
    saisie = st.text_input("Exemple: 2 5 8 11", value="2 5 8 11")
    
    if st.button("Analyser la suite"):
        try:
            # Conversion en liste de nombres
            termes = [float(x) for x in saisie.strip().split()]
            
            if len(termes) < 2:
                st.warning("⚠️ Il faut au moins 2 valeurs pour définir une suite.")
                return
            
            # Analyse
            raison = termes[1] - termes[0]
            est_arithmetique = True
            
            for i in range(len(termes) - 1):
                diff = termes[i+1] - termes[i]
                if not math.isclose(diff, raison, abs_tol=1e-9):
                    est_arithmetique = False
                    st.error(f"❌ Ce n'est **PAS** une suite arithmétique.")
                    st.write(f"L'écart change : {raison} au début, puis {diff}.")
                    break
            
            if est_arithmetique:
                st.success("✅ C'est une suite **ARITHMÉTIQUE**.")
                
                col1, col2 = st.columns(2)
                col1.metric("Premier terme ($u_0$)", f"{termes[0]:g}")
                col2.metric("Raison ($r$)", f"{raison:g}")
                
                st.subheader("Les 10 premiers termes")
                
                # Calcul des termes suivants
                u0 = termes[0]
                n_vals = list(range(10))
                u_vals = [u0 + n * raison for n in n_vals]
                
                # Création d'un DataFrame pour l'affichage
                df = pd.DataFrame({"n": n_vals, "u_n": u_vals})
                
                # Affichage table + graphique côte à côte
                col_table, col_chart = st.columns([1, 2])
                col_table.dataframe(df.style.format({"u_n": "{:.2f}"}), hide_index=True)
                col_chart.line_chart(df.set_index("n"))

        except ValueError:
            st.error("Erreur de format : Entrez uniquement des nombres séparés par des espaces.")

# --- 3. FONCTIONS AFFINES ---
def page_fonctions():
    show_header("Fonctions Affines", "📉")
    
    st.info("Ajoutez des points (x, y) pour vérifier s'ils forment une droite.")

    # Création d'un tableau éditable pour saisir les points
    default_data = pd.DataFrame({"x": [0.0, 1.0, 2.0], "y": [1.0, 3.0, 5.0]})
    df_input = st.data_editor(default_data, num_rows="dynamic", key="affine_editor")

    if st.button("Analyser la fonction"):
        if len(df_input) < 2:
            st.warning("⚠️ Il faut au moins 2 points.")
            return

        X = df_input["x"].values
        Y = df_input["y"].values

        # Vérification x1 != x0
        if X[1] == X[0]:
            st.error("Erreur : Droite verticale (division par zéro).")
            return

        # Calcul coef directeur (a) et ordonnée à l'origine (b)
        a = (Y[1] - Y[0]) / (X[1] - X[0])
        b = Y[0] - (a * X[0])

        est_affine = True
        
        # Vérification de tous les points
        for i in range(len(X)):
            y_calcul = a * X[i] + b
            if not math.isclose(Y[i], y_calcul, abs_tol=1e-9):
                est_affine = False
                st.error("❌ Ce n'est **PAS** une fonction affine unique.")
                st.write(f"Le point ({X[i]}, {Y[i]}) n'est pas aligné avec les premiers points.")
                st.markdown(f"La droite théorique serait : $y = {a:g}x + {b:g}$")
                break
        
        if est_affine:
            st.success("✅ C'est une fonction **AFFINE**.")
            
            signe_b = "+ " if b >= 0 else ""
            st.latex(f"f(x) = {a:g}x {signe_b} {b:g}")
            
            col1, col2 = st.columns(2)
            col1.metric("Coefficient ($a$)", f"{a:g}")
            col2.metric("Ordonnée ($b$)", f"{b:g}")

            # Visualisation graphique avec Matplotlib pour plus de contrôle
            fig, ax = plt.subplots()
            ax.plot(X, Y, 'o-', label='Points saisis', color='blue')
            
            # Étendre un peu la ligne pour visualiser la tendance
            x_min, x_max = min(X) - 1, max(X) + 1
            y_min = a * x_min + b
            y_max = a * x_max + b
            ax.plot([x_min, x_max], [y_min, y_max], '--', color='red', alpha=0.5, label='Droite')
            
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            ax.grid(True)
            
            st.pyplot(fig)

# --- MENU PRINCIPAL (Sidebar) ---
def main():
    st.sidebar.title("Super Calc Maths 🚀")
    choix = st.sidebar.radio(
        "Menu", 
        ["Probabilités", "Suites", "Fonctions Affines"]
    )
    
    st.sidebar.info("Application compatible Mobile & PC")

    if choix == "Probabilités":
        page_probabilites()
    elif choix == "Suites":
        page_suites()
    elif choix == "Fonctions Affines":
        page_fonctions()

if __name__ == "__main__":
    main()