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

# --- 4. CALCULATEUR DE MOYENNE ---
def page_moyenne():
    show_header("Calculateur de Moyenne", "🎓")
    st.markdown("Rentre tes notes et coefficients dans le tableau ci-dessous.")
    
    # Création d'un tableau vide par défaut
    default_notes = pd.DataFrame({
        "Matière": ["Maths", "E.S", "Anglais","Espagnol", "EPS", "Français", "Hist-Geo", "EMC", "LLCE Espagnol", "SVT", "Cinéma" ],
        "Note": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        "Coefficient": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    })
    
    # Tableau éditable
    df_notes = st.data_editor(
        default_notes, 
        num_rows="dynamic", 
        column_config={
            "Note": st.column_config.NumberColumn("Note (/20)", min_value=0, max_value=20, step=0.25),
            "Coefficient": st.column_config.NumberColumn("Coefficient", min_value=1, step=1)
        },
        key="moyenne_editor"
    )

    if st.button("Calculer ma moyenne"):
        if df_notes.empty:
            st.warning("Ajoute des notes pour calculer la moyenne.")
        else:
            # Calcul mathématique : Somme(Note * Coeff) / Somme(Coeff)
            total_points = (df_notes["Note"] * df_notes["Coefficient"]).sum()
            total_coeffs = df_notes["Coefficient"].sum()
            
            if total_coeffs == 0:
                st.error("Le total des coefficients ne peut pas être zéro.")
            else:
                moyenne = total_points / total_coeffs
                
                # Affichage du résultat
                st.markdown("---")
                col_res1, col_res2 = st.columns([1, 2])
                
                with col_res1:
                    st.metric(label="Moyenne Générale", value=f"{moyenne:.2f} / 20")
                
                with col_res2:
                    # Message personnalisé selon la note (Mentions)
                    if moyenne < 10:
                        st.error(f"Courage ! Il manque {10 - moyenne:.2f} points pour la moyenne.")
                    elif 10 <= moyenne < 12:
                        st.warning("Tu as la moyenne !")
                    elif 12 <= moyenne < 14:
                        st.info("Mention Assez Bien ! Bravo !")
                    elif 14 <= moyenne < 16:
                        st.success("Mention Bien ! Super boulot !")
                    else:
                        st.balloons()
                        st.success("Mention Très Bien ! Excellent !!")
                
                # Barre de progression visuelle
                st.progress(min(moyenne / 20, 1.0))

# --- 5. BOUTIQUE DE PERLES ---
def page_boutique():
    show_header("Gestion Boutique Perles", "💎")
    if 'stock_perles' not in st.session_state:
        st.session_state.stock_perles = pd.DataFrame({
            "Nom de la Perle": ["Charms nœud de papillon", "Charms étoile", "Cœur magnétique", "Perle cristal 3mm", "Aiguille bout rond"],
            "Prix Unitaire (€)": [0.0625, 0.0132, 0.085, 0.01, 0.01]
        })

    # Initialisation du projet actuel
    if 'projet_actuel' not in st.session_state:
        st.session_state.projet_actuel = pd.DataFrame([{"Perle" : "Charms nœud de papillon" "Charms étoile" "Cœur magnétique" "Perle cristal 3mm" "Aiguille bout rond", "Quantité": 1}])

    tab_stock, tab_calcul = st.tabs(["📦 Mon Stock", "💍 Calculateur Prix & Temps"])

    with tab_stock:
        st.subheader("Répertoire des prix")
        st.caption("Modifie les prix ici. Ils seront sauvegardés tant que l'appli est ouverte.")
        st.session_state.stock_perles = st.data_editor(
            st.session_state.stock_perles, 
            num_rows="dynamic",
            key="editor_stock"
        )

    with tab_calcul:
        st.subheader("1. Matériel utilisé")
        liste_noms = st.session_state.stock_perles["Nom de la Perle"].tolist()
        
        if not liste_noms:
            st.warning("Le stock est vide !")
        else:
            # Éditeur pour choisir les perles du bijou
            projet_df = st.data_editor(
                st.session_state.projet_actuel,
                num_rows="dynamic",
                column_config={
                    "Perle": st.column_config.SelectboxColumn("Perle", options=liste_noms, required=True),
                    "Quantité": st.column_config.NumberColumn("Quantité", min_value=1, step=1)
                },
                key="calculateur_projet_editor"
            )
            # Sauvegarde de l'état pour ne pas perdre la saisie
            st.session_state.projet_actuel = projet_df

            st.markdown("---")
            st.subheader("2. Main d'œuvre (Temps passé)")
            
            c_taux, c_h, c_m = st.columns(3)
            taux_horaire = c_taux.number_input("Taux horaire (€/h)", min_value=0.0, value=10.0, step=0.5, help="Combien veux-tu gagner par heure ?")
            heures = c_h.number_input("Heures", min_value=0, value=0, step=1)
            minutes = c_m.number_input("Minutes", min_value=0, max_value=59, value=30, step=5)

            if st.button("💰 Calculer le PRIX FINAL"):
                # Calcul Matériel
                stock = st.session_state.stock_perles
                # Fusionner le projet avec le stock pour avoir les prix
                resultat = projet_df.merge(stock, left_on="Perle", right_on="Nom de la Perle", how="left")
                
                # Gestion des perles introuvables (si on a supprimé du stock entre temps)
                if resultat["Prix Unitaire (€)"].isnull().any():
                    st.error("Attention : Certaines perles du projet ne sont plus dans le stock !")
                else:
                    cout_materiel = (resultat["Quantité"] * resultat["Prix Unitaire (€)"]).sum()
                    
                    # Calcul Main d'œuvre
                    temps_total_heures = heures + (minutes / 60.0)
                    cout_travail = temps_total_heures * taux_horaire
                    
                    # Totaux
                    cout_de_revient = cout_materiel + cout_travail
                    prix_vente = cout_de_revient * 2
                    
                    # --- AFFICHAGE DES RÉSULTATS ---
                    st.markdown("### 🧾 Résultat")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Coût Matériel", f"{cout_materiel:.2f} €")
                    col2.metric("Coût Travail", f"{cout_travail:.2f} €", help=f"{heures}h{minutes} à {taux_horaire}€/h")
                    col3.metric("Coût de Revient Total", f"{cout_de_revient:.2f} €", delta="Coût réel")
                    
                    st.success(f"**✨ PRIX DE VENTE CONSEILLÉ (x2) : {prix_vente:.2f} € ✨**")
                    st.caption(f"Ce prix inclut tes perles, ton temps de travail ({cout_travail:.2f}€) et une marge de bénéfice de {prix_vente - cout_de_revient:.2f}€.")

# --- MENU PRINCIPAL (Sidebar) ---
def main():
    st.sidebar.title("Super Calc Maths Pour Ma Nana <3")
    
    # Mise à jour du menu avec la nouvelle option
    choix = st.sidebar.radio("Menu", ["Probabilités", "Suites", "Fonctions Affines", "Moyenne Scolaire", "Boutique de Perles"])
    
    st.sidebar.info("Application compatible Mobile & PC")

    if choix == "Probabilités":
        page_probabilites()
    elif choix == "Suites":
        page_suites()
    elif choix == "Fonctions Affines":
        page_fonctions()
    elif choix == "Moyenne Scolaire":  # Appel de la nouvelle page
        page_moyenne()
    elif choix == "Boutique de Perles":
        page_boutique()


if __name__ == "__main__":
    main()










