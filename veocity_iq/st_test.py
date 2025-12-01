import streamlit as st

st.set_page_config(page_title="Supercar Chatbot", layout="wide")

st.title("🏎️ Supercar Chatbot")
st.write("Ask me anything about supercars — specifications, history, price, engines, inventions, founders, and more.")

# --- Chatbot Logic ---
def get_response(user_msg):
    msg = user_msg.lower()

    # ----------------- FERRARI -----------------
    if "ferrari" in msg:
        if "price" in msg:
            return "Ferrari prices start from ₹4 Crore in India (F8 Tributo) and go up to ₹10–20 Crore for limited editions like LaFerrari."
        elif "founder" in msg or "invention" in msg:
            return "Ferrari was founded in 1939 by Enzo Ferrari. The company started racing before producing road cars."
        elif "engine" in msg:
            return "Ferrari is famous for its V8 twin-turbo engines and iconic high-revving V12s like the 812 Superfast."
        else:
            return "Ferrari is known for F1 heritage, sharp handling, and cars like LaFerrari, SF90 Stradale, and F8 Tributo."

    # ----------------- LAMBORGHINI -----------------
    elif "lamborghini" in msg or "lambo" in msg:
        if "price" in msg:
            return "Lamborghini prices start from around ₹4 Crore (Huracan) and can exceed ₹8–10 Crore for Aventador/Revuelto."
        elif "founder" in msg or "invention" in msg:
            return "Automobili Lamborghini was founded by Ferruccio Lamborghini in 1963 after a disagreement with Enzo Ferrari."
        elif "engine" in msg:
            return "Lamborghini uses naturally aspirated V10 engines (Huracan) and V12 engines (Aventador/Revuelto)."
        else:
            return "Lamborghini is known for aggressive designs, scissor doors, and brutal V10/V12 performance."

    # ----------------- MCLAREN -----------------
    elif "mclaren" in msg:
        if "price" in msg:
            return "McLaren prices start from ₹3.5 Crore (570S era) and go up to ₹15+ Crore for models like the McLaren P1."
        elif "founder" in msg or "invention" in msg:
            return "McLaren was founded by Bruce McLaren in 1963. Known for its carbon-fiber innovation and F1 racing success."
        elif "engine" in msg:
            return "McLaren uses twin-turbo V8 engines across most models, delivering exceptional power-to-weight ratios."
        else:
            return "McLaren is known for lightweight engineering, active aerodynamics, and cars like 720S, P1, and Artura."

    # ----------------- ROLLS ROYCE -----------------
    elif "rolls" in msg or "rolls royce" in msg:
        if "price" in msg:
            return "Rolls-Royce prices start around ₹6.5 Crore (Ghost) and go beyond ₹10–12 Crore for Phantom and Cullinan."
        elif "founder" in msg or "invention" in msg:
            return "Rolls-Royce was founded by Charles Rolls and Henry Royce in 1904, focusing on unmatched luxury and craftsmanship."
        elif "engine" in msg:
            return "Rolls-Royce uses smooth V12 twin-turbo engines for effortless, silent performance."
        else:
            return "Rolls-Royce is known for ultimate luxury, hand-built cars, starlight headliners, and the iconic Spirit of Ecstasy."

    # ----------------- BUGATTI -----------------
    elif "bugatti" in msg:
        if "price" in msg:
            return "Bugatti prices begin around ₹30–40 Crore. Limited editions can exceed ₹100 Crore (La Voiture Noire)."
        elif "founder" in msg or "invention" in msg:
            return "Bugatti was founded by Ettore Bugatti in 1909, known for engineering masterpieces and extreme performance."
        elif "engine" in msg:
            return "Bugatti uses a quad-turbo W16 8.0L engine producing 1500+ HP in the Chiron and 1200 HP in the Veyron."
        elif "fastest" in msg:
            return "The Bugatti Chiron Super Sport 300+ hit 304 mph (490 km/h), one of the fastest production cars ever."
        else:
            return "Bugatti builds hypercars with insane engineering — Veyron, Chiron, Divo, Bolide."

    # ----------------- ASTON MARTIN -----------------
    elif "aston" in msg or "aston martin" in msg:
        if "price" in msg:
            return "Aston Martin prices start around ₹3.5 Crore and go up to ₹10+ Crore for models like the Valkyrie."
        elif "founder" in msg or "invention" in msg:
            return "Aston Martin was founded in 1913 by Lionel Martin and Robert Bamford. Known for elegance and British craftsmanship."
        elif "engine" in msg:
            return "Aston Martin uses V8 twin-turbo engines (AMG-sourced) and powerful V12 engines in flagship models."
        else:
            return "Aston Martin is known for luxury GT cars like DB11, Vantage, and the hypercar Valkyrie."

    # ----------------- AUDI (Performance) -----------------
    elif "audi" in msg:
        if "price" in msg:
            return "Audi RS models start around ₹1.2–2 Crore. The Audi R8 was around ₹2.5–3 Crore before discontinuation."
        elif "engine" in msg:
            return "Audi RS cars use turbocharged inline-5, V6, and V8 engines. The Audi R8 used a naturally aspirated V10."
        elif "founder" in msg or "invention" in msg:
            return "Audi was founded by August Horch in 1909. Known for quattro AWD and German engineering."
        else:
            return "Audi performance cars include RS7, RS6 Avant, RSQ8, and the legendary Audi R8 V10."

    # ---------------- DEFAULT ----------------
    elif "fastest" in msg:
        return "The fastest production cars include Bugatti Chiron Super Sport 300+, Koenigsegg Jesko Absolut, and SSC Tuatara."

    else:
        return "I don’t know that yet, but ask me anything related to supercars — price, history, engines, founders, or comparisons."


# ---------------- STREAMLIT UI ----------------
user_input = st.text_input("Your message:", "")

if st.button("Send"):
    if user_input.strip() != "":
        response = get_response(user_input)
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**Chatbot:** {response}")
