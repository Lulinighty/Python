import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Super Maths For Nana <3",
    page_icon="🧮",
    layout="centered"
)

# --- FONCTION POUR DESSINER L'ARBRE ---
def dessiner_arbre(p_a, p_b_a, p_b_non_a):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Coordonnées des points (X, Y)
    start = (0, 0.5)
    end_a = (1, 0.75)
    end_non_a = (1, 0.25)
    end_b_a = (2, 0.85)
    end_non_b_a = (2, 0.65)
    end_b_non_a = (2, 0.35)
    end_non_b_non_a = (2, 0.15)

    # Fonction interne pour tracer une branche
    def tracer_branche(start, end, text_prob, text_event):
        ax.plot([start[0], end[0]], [start[1], end[1]], color="black", lw=2)
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y + 0.03, text_prob, ha='center', color='blue', fontsize=10)
        ax.text(end[0] + 0.05, end[1], text_event, ha='left', va='center', fontsize=12, fontweight='bold')

    # Branche A et non A
    tracer_branche(start, end_a, f"{p_a:g}", "A")
    tracer_branche(start, end_non_a, f"{1-p_a:g}", "Ā")

    # Branches B sachant A
    tracer_branche(end_a, end_b_a, f"{p_b_a:g}", "B")
    tracer_branche(end_a, end_non_b_a, f"{1-p_b_a:g}", "B̄")

    # Branches B sachant non A
    tracer_branche(end_non_a, end_b_non_a, f"{p_b_non_a:g}", "B")
    tracer_branche(end_non_a, end_non_b_non_a, f"{1-p_b_non_a:g}", "B̄")

    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

# Fonction utilitaire pour le style
def show_header(title, emoji):
    st.markdown(f"## {emoji} {title}")
    st.markdown("---")

# --- 1. PROBABILITÉS ---
def page_probabilites():
    show_header("Probabilités", "🎲")
    
    # Ajout de l'onglet "Arbre" ici
    tab1, tab2, tab3, tab4 = st.tabs(["Simple", "Combinatoire", "Binomiale", "🌳 Arbre"])
    
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

    with tab4:
        st.subheader("Générateur d'Arbre")
        col_a, col_b_a, col_b_na = st.columns(3)
        pa = col_a.number_input("P(A)", 0.0, 1.0, 0.5, 0.05)
        pba = col_b_a.number_input("P(B|A)", 0.0, 1.0, 0.7, 0.05)
        pbna = col_b_na.number_input("P(B|Ā)", 0.0, 1.0, 0.4, 0.05)
        
        fig = dessiner_arbre(pa, pba, pbna)
        st.pyplot(fig)
        
        # Calculs de l'arbre
        st.info("💡 **Calculs des intersections :**")
        p_a_inter_b = pa * pba
        p_na_inter_b = (1 - pa) * pbna
        st.latex(f"P(A \\cap B) = {pa:g} \\times {pba:g} = {p_a_inter_b:g}")
        st.latex(f"P(\\bar{{A}} \\cap B) = {1-pa:g} \\times {pbna:g} = {p_na_inter_b:g}")
        st.success(f"**Probabilité totale P(B) = {p_a_inter_b + p_na_inter_b:g}**")

# --- 2. SUITES ARITHMÉTIQUES ---
def page_suites():
    show_header("Suites Arithmétiques", "📊")
    st.markdown("Entrez les premiers termes séparés par un espace.")
    saisie = st.text_input("Exemple: 2 5 8 11", value="2 5 8 11")
    
    if st.button("Analyser la suite"):
        try:
            termes = [float(x) for x in saisie.strip().split()]
            if len(termes) < 2:
                st.warning("⚠️ Il faut au moins 2 valeurs pour définir une suite.")
                return
            
            raison = termes[1] - termes[0]
            est_arithmetique = True
            for i in range(len(termes) - 1):
                diff = termes[i+1] - termes[i]
                if not math.isclose(diff, raison, abs_tol=1e-9):
                    est_arithmetique = False
                    st.error(f"❌ Ce n'est **PAS** une suite arithmétique.")
                    break
            
            if est_arithmetique:
                st.success("✅ C'est une suite **ARITHMÉTIQUE**.")
                col1, col2 = st.columns(2)
                col1.metric("Premier terme ($u_0$)", f"{termes[0]:g}")
                col2.metric("Raison ($r$)", f"{raison:g}")
                
                u0 = termes[0]
                n_vals = list(range(10))
                u_vals = [u0 + n * raison for n in n_vals]
                df = pd.DataFrame({"n": n_vals, "u_n": u_vals})
                col_table, col_chart = st.columns([1, 2])
                col_table.dataframe(df.style.format({"u_n": "{:.2f}"}), hide_index=True)
                col_chart.line_chart(df.set_index("n"))
        except ValueError:
            st.error("Erreur de format : Entrez uniquement des nombres.")

# --- 3. FONCTIONS AFFINES ---
def page_fonctions():
    show_header("Fonctions Affines", "📉")
    st.info("Ajoutez des points (x, y) pour vérifier s'ils forment une droite.")
    default_data = pd.DataFrame({"x": [0.0, 1.0, 2.0], "y": [1.0, 3.0, 5.0]})
    df_input = st.data_editor(default_data, num_rows="dynamic", key="affine_editor")

    if st.button("Analyser la fonction"):
        if len(df_input) < 2:
            st.warning("⚠️ Il faut au moins 2 points.")
            return
        X = df_input["x"].values
        Y = df_input["y"].values
        if X[1] == X[0]:
            st.error("Erreur : Droite verticale.")
            return
        a = (Y[1] - Y[0]) / (X[1] - X[0])
        b = Y[0] - (a * X[0])
        est_affine = True
        for i in range(len(X)):
            y_calcul = a * X[i] + b
            if not math.isclose(Y[i], y_calcul, abs_tol=1e-9):
                est_affine = False
                st.error("❌ Ce n'est **PAS** une fonction affine unique.")
                break
        
        if est_affine:
            st.success("✅ C'est une fonction **AFFINE**.")
            signe_b = "+ " if b >= 0 else ""
            st.latex(f"f(x) = {a:g}x {signe_b} {b:g}")
            fig, ax = plt.subplots()
            ax.plot(X, Y, 'o-', label='Points saisis', color='blue')
            ax.grid(True)
            st.pyplot(fig)

# --- MENU PRINCIPAL (Sidebar) ---
def main():
    st.sidebar.title("Super Calc Maths Pour Ma Nana <3")
    choix = st.sidebar.radio("Menu", ["Probabilités", "Suites", "Fonctions Affines"])
    st.sidebar.info("Application compatible Mobile & PC")

    if choix == "Probabilités":
        page_probabilites()
    elif choix == "Suites":
        page_suites()
    elif choix == "Fonctions Affines":
        page_fonctions()

if __name__ == "__main__":
    main()
