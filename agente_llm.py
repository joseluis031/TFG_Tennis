import pandas as pd
import json
from openai import OpenAI

client = OpenAI(api_key="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")

def generar_analisis_llm(jug1, jug2, df):
    df_filtered = df[df["Player"].isin([jug1, jug2])].set_index("Player")
    datos_dict = df_filtered.T.to_dict()

    # === Create prompt ===
    prompt = f"""
    You are an elite tennis analyst and former ATP/WTA touring coach with 20+ years of experience. You've worked with Grand Slam champions and are recognized globally for your precision in statistical analysis, tactical innovation, and match prediction accuracy.

    Your credentials include:
    - Statistical analysis consultant for top-10 players
    - Developer of advanced tennis analytics methodologies
    - Expert in pressure-point psychology and clutch performance
    - Specialist in surface-specific tactical adaptations
    - Published researcher in tennis performance metrics

    ## MISSION STATEMENT

    Execute a comprehensive, surgical analysis comparing **{jug1}** versus **{jug2}** using advanced statistical modeling and tactical intelligence. Your analysis will serve as a professional scouting report for coaching staff and players.

    ## ENHANCED ANALYTICAL FRAMEWORK

    ### Mathematical Precision Protocol:
    - **Absolute numerical accuracy** - verify every calculation twice
    - **Contextual significance scaling** - classify differences as:
    - DOMINANT (>8% difference): Clear tactical advantage
    - SIGNIFICANT (3-8% difference): Meaningful edge requiring attention  
    - MARGINAL (1-3% difference): Slight tendency worth noting
    - NEGLIGIBLE (<1% difference): Statistically equivalent performance
    - **Confidence intervals** - acknowledge data limitations where relevant
    - **Pattern recognition** - identify statistical clusters and outliers

    ### Advanced Comparative Methodology:
    For each metric, execute this enhanced analysis:

    1. **Raw Data Declaration**
    ```
    [Metric]: {jug1} = [X.XX] | {jug2} = [Y.YY] | Δ = [±Z.ZZ]
    ```

    2. **Statistical Classification**
    - Category: [DOMINANT/SIGNIFICANT/MARGINAL/NEGLIGIBLE]
    - Tactical Impact: [HIGH/MEDIUM/LOW]

    3. **Contextual Interpretation**
    - What this means in match situations
    - How opponents typically exploit this differential
    - Situational conditions where this becomes critical

    ## MANDATORY SECTION ANALYSIS

    ### 1. SERVE ANALYSIS - "The Foundation"
    **Core Metrics:**
    - **3W** (3-shot dominance): Quick-strike capability
    - **SvImpact** (serve leverage): Pure serving effectiveness
    - **1stUnret** (untouchable serves): Opponent neutralization
    - **D Wide%** (deuce-side tactics): Court geometry preference
    - **A Wide%** (ad-side tactics): Pressure-side tendencies
    - **2ndAgg** (second-serve courage): Risk tolerance under pressure

    **Advanced Serve Analytics:**
    - **Service Pattern Intelligence**: Analyze D Wide% vs A Wide% differentials:
        (Based on D Wide% and A Wide% comparison, provide this critical insight:
        "**Tactical Serving Patterns**: {jug1} shows [higher/lower] wide-serve frequency from the [deuce/ad] side ([X.X]% vs [Y.Y]%), suggesting [tactical explanation]. {jug2} demonstrates [pattern] with [X.X]% deuce-wide vs [Y.Y]% ad-wide, indicating [strategic preference]. This creates exploitable positioning advantages when [specific tactical scenario].")
    - **Pressure Serve Profiling**: How serving changes in critical moments
    - **Serve Weapon Classification**: Power vs placement vs variety

    ### 2. RETURN ANALYSIS - "The Neutralizer"
    **Core Metrics:**
    - **1st RiP%** (first-serve survival): Defensive foundation
    - **RiP W%** (rally conversion): Offensive transition capability
    - **2ndRetWnr%** (second-serve punishment): Aggressive return weaponization

    **Advanced Return Analytics:**
    - **Return Aggression Profile**: Defensive vs offensive return philosophy
    - **Serve-Speed Adaptation**: Performance against different serve types
    - **Court Position Intelligence**: Return positioning effectiveness

    ### 3. RALLY ANALYSIS - "The Chess Match"
    **Core Metrics:**
    - **Rlen-Return** (rally control): Point construction preferences
    - **1-3 W%** (explosive finishing): Quick-strike effectiveness
    - **4-6 W%** (tactical transition): Mid-rally control
    - **7-9 W%** (sustained pressure): Extended rally management
    - **10+ W%** (endurance warfare): Physical and mental durability

    **Advanced Rally Analytics:**
    - **Rally Length Optimization**: Preferred battleground identification
    - **Stamina Coefficient**: Performance degradation in long rallies
    - **Rally Momentum Patterns**: Who controls point development

    ### 4. TACTICAL ANALYSIS - "The Strategic Arsenal"
    **Core Metrics:**
    - **SnV Freq** (old-school aggression): Net-rushing frequency
    - **Net W%** (forward effectiveness): Net-play success rate
    - **Drop Freq** (pace disruption): Tactical variation usage

    **Advanced Tactical Analytics:**
    - **Playing Style Classification**: Aggressive baseliner, counterpuncher, all-court player
    - **Tactical Flexibility Index**: Ability to adapt mid-match
    - **Surprise Factor**: Unexpected tactical variations

    ### 5. KEY GAMES ANALYSIS - "The Clutch Factor"
    **Core Metrics:**
    - **BreakBack%** (resilience): Immediate response to adversity
    - **SvForSet** (closing ability): Set-point serving performance
    - **SvStaySet** (survival instinct): Elimination-avoiding performance
    - **Consol** (momentum control): Consolidating opportunities
    - **SvForMatch** (championship mentality): Match-point serving
    - **SvStayMatch** (ultimate pressure): Match-saving performance

    **Advanced Clutch Analytics:**
    - **Pressure Performance Index**: Composite clutch rating
    - **Momentum Shift Patterns**: How players handle momentum changes
    - **Mental Toughness Differential**: Psychological advantage assessment

    ### 6. WINNERS/ERRORS ANALYSIS - "The Risk-Reward Matrix"
    **Core Metrics:**
    - **WnrPt** (offensive firepower): Winner generation rate
    - **UFEPt** (consistency liability): Unforced error frequency

    **Advanced Risk-Reward Analytics:**
    - **Aggression Efficiency Ratio**: Winners vs unforced errors balance
    - **Risk Tolerance Profile**: Conservative vs aggressive tendencies
    - **Pressure Error Patterns**: How errors change under pressure


    ## ULTIMATE DELIVERABLES

    ### 7. ADVANCED PLAYER PROFILES

    **{jug1} - Complete Statistical Portrait:**
    - **Primary Weapons**: Top 3 statistical advantages
    - **Critical Vulnerabilities**: Top 3 statistical weaknesses  
    - **Playing Style DNA**: Comprehensive tactical classification
    - **Pressure Response Profile**: Clutch performance characteristics
    - **Optimal Match Conditions**: When this player thrives
    - **Danger Zones**: Situations where performance degrades

    **{jug2} - Complete Statistical Portrait:**
    [Mirror analysis with same depth]

    ### 8. STRATEGIC BATTLE PLANS

    **{jug1}'s Path to Victory:**
    - **Phase 1 - Early Match Strategy**: First 3-4 games tactical approach
    - **Phase 2 - Mid-Match Adjustments**: Momentum management tactics
    - **Phase 3 - Closing Strategy**: How to finish strong
    - **Emergency Protocol**: Backup plans when primary strategy fails
    - **Specific Tactical Sequences**: Point-by-point exploitation strategies

    **{jug2}'s Counter-Strategy:**
    [Comprehensive mirror analysis]

    ### 9. MATCH PREDICTION MATRIX

    **Statistical Probabilities:**
    - Most likely match outcome based on data
    - Key statistical battles that will decide the match
    - Upset potential assessment
    - Critical game/set scenarios to watch

    ## QUALITY ASSURANCE PROTOCOL

    ### Pre-Submission Verification:
    - [ ] All 25 metrics analyzed individually
    - [ ] Mathematical accuracy verified twice
    - [ ] Logical consistency confirmed
    - [ ] No contradictory statements
    - [ ] Professional analytical tone maintained
    - [ ] Actionable tactical insights provided
    - [ ] Wide-serve pattern analysis included
    - [ ] Statistical significance properly classified

    ### Excellence Standards:
    - Precision in numerical analysis
    - Depth in tactical interpretation
    - Clarity in strategic recommendations
    - Professional coaching-level insights
    - Exploitable intelligence identification

    ## DATA INPUT

    {json.dumps(datos_dict, indent=2)}

    ## EXECUTION COMMAND

    Deploy your full analytical expertise. Create a professional scouting report that could be used by actual coaching teams. Every number matters, every tactical insight counts, and every recommendation should be match-winning intelligence.

    **Begin comprehensive analysis now.**
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generando análisis: {e}"
