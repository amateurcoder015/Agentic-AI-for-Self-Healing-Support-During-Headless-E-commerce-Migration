from agent import observe, embed, cluster, reason, decide
from agent import llm_mock, counterfactual, trajectory, repro_pack 
# Removed digital_twin import

def print_agent_report(analysis, decision, alternatives, trend_info, restraint):
    """
    EXPLAIN: Renders the strict 'Agentic Incident Analysis' format.
    """
    print("\n" + "="*50)
    print("=== AGENTIC INCIDENT ANALYSIS ===")
    print("="*50)

    print("\nPRIMARY ASSESSMENT:")
    print(f"- Stage:      {analysis['stage']}")
    print(f"- Root Cause: {analysis['root_cause']}")
    print(f"- Confidence: {analysis['confidence']} (LLM-Verified)")

    print("\nEVIDENCE & SIGNALS:")
    print(f"- Cluster Size:    {analysis['ticket_count']} tickets")
    print(f"- Dominant Terms:  {analysis.get('reasoning', 'N/A')}")
    print(f"- Signal Trend:    {trend_info['trajectory']}")

    print("\nALTERNATE HYPOTHESES CONSIDERED:")
    for idx, alt in enumerate(alternatives, 1):
        print(f"{idx}. {alt['hypothesis']}")
        print(f"   REJECTED: {alt['reason_rejected']}")

    print("\nPROACTIVE / REACTIVE DECISION:")
    print(f"- Action taken: {decision['recommended_action']}")
    print(f"- Risk level:   {decision['risk_level']}")

    print("\nAUTOMATION RESTRAINT:")
    print(f"- Action NOT taken: {restraint['action_not_taken']}")
    print(f"- Reason:           {restraint['reason']}")

    print("\nPROJECTED OUTCOME:")
    print(f"- Expectation: {trend_info['prediction']}")
    print("="*50 + "\n")


def generate_restraint_logic(risk_level, confidence):
    """
    DECIDE (Restraint): Explicitly explains what the agent WON'T do.
    """
    # Safety casting
    try:
        conf_val = float(confidence)
    except:
        conf_val = 0.5

    if risk_level == "High":
        return {
            "action_not_taken": "Auto-Rollback of API Deployment",
            "reason": "Risk is Critical, but human approval is required for non-safe rollback operations."
        }
    elif conf_val < 0.8:
        return {
            "action_not_taken": "Auto-Email Blast to Merchants",
            "reason": f"Confidence ({conf_val}) is below the 0.8 threshold for automated external comms."
        }
    else:
        return {
            "action_not_taken": "Escalation to VP Engineering",
            "reason": "Issue severity (Medium/Low) does not meet SLA requirements for executive wake-up."
        }

def main():
    print("Initializing Agentic System...\n")

    # 1. OBSERVE
    tickets = observe.load_tickets()
    signals = observe.load_system_signals()

    # 2. VECTORIZE & CLUSTER
    embeddings = embed.generate_embeddings(tickets)
    clusters = cluster.cluster_tickets(tickets, embeddings)

    # 3. ANALYZE SYSTEM TRAJECTORY (Global Context)
    traj_label, prediction = trajectory.analyze_signal_trend(signals)
    trend_info = {"trajectory": traj_label, "prediction": prediction}

    # 4. AGENT LOOP OVER CLUSTERS
    for label, cluster_tickets in clusters.items():
        if label == -1: continue # Skip noise for the deep report

        # A. AGGREGATE TEXT
        cluster_text = " ".join([t['message'] for t in cluster_tickets])

        # B. HYBRID REASONING (Rule + LLM)
        llm_analysis = llm_mock.analyze_cluster_semantically(cluster_text)
        llm_analysis['ticket_count'] = len(cluster_tickets)

        # C. COUNTERFACTUAL REASONING
        alternatives = counterfactual.generate_alternatives(
            llm_analysis['root_cause'], 
            cluster_text
        )

        # D. DECIDE ACTION
        decision = decide.determine_action(llm_analysis)

        # (Digital Twin Analysis Removed)

        # E. AUTOMATION RESTRAINT
        restraint = generate_restraint_logic(
            decision['risk_level'], 
            llm_analysis['confidence']
        )

        # F. EXPLAIN / OUTPUT
        print_agent_report(llm_analysis, decision, alternatives, trend_info, restraint)

        # G. REPRO PACK GENERATION (Conditional)
        conf_val = float(llm_analysis.get('confidence', 0))
        is_stage_3 = "Stage 3" in llm_analysis.get('stage', '')
        is_platform_issue = "Platform Issue" in llm_analysis.get('root_cause', '')

        if is_stage_3 and is_platform_issue and conf_val >= 0.8:
            path, inc_id, r_type, triggers = repro_pack.generate_repro_pack(
                llm_analysis, 
                cluster_tickets, 
                signals
            )
            
            header_suffix = "(Preliminary)" if r_type == "preliminary" else ""
            print(f"REPRODUCTION PACK GENERATED {header_suffix}")
            print(f"- Incident ID: {inc_id}")
            print(f"- Saved to:    {path}")
            print(f"- Type:        {r_type.title()}")
            print(f"- Triggers:    {', '.join(triggers)}")
            print("-" * 50)

if __name__ == "__main__":
    main()