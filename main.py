from agent import observe, embed, cluster, reason, decide

def generate_global_insight(all_analyses):
    """
    ACT (Global): triggers alerts ONLY if strict criteria are met.
    """
    print("\n" + "="*60)
    print("GLOBAL SYSTEM HEALTH CHECK")
    print("="*60)
    
    severe_alerts = []
    
    for a in all_analyses:
        # --- UPDATED GLOBAL ALERT LOGIC ---
        # 1. Ignore Noise (-1)
        # 2. Ignore small clusters (< 3 tickets)
        # 3. Must be Stage 3 (Live)
        # 4. Must have High Confidence (>= 0.7)
        # 5. Must be a Platform Issue
        if (a['cluster_label'] != -1 and 
            a['ticket_count'] >= 3 and
            "Stage 3" in a['stage'] and
            a['confidence_score'] >= 0.7 and 
            "Platform" in a['root_cause']):
            
            severe_alerts.append(a)

    if severe_alerts:
        print(f"🚨 CRITICAL ALERT: {len(severe_alerts)} Verified Production Outage(s) Detected.")
        print("   Logic: High-confidence clusters matching Stage 3 regression patterns.")
        print("   RECOMMENDATION: FREEZE DEPLOYMENTS & PAGE ON-CALL ENGINEERING.")
    else:
        # Fallback for standard insights
        print("✅ STATUS: Operational. No critical platform outages detected.")
        print("   NOTE: Monitoring standard support volume.")

def run_proactive_check(signals, all_analyses):
    """
    REASON (Phase 2): Checks for high-error signals NOT yet reflected in tickets.
    """
    if not signals:
        return

    # 1. Check Signal Threshold
    checkout_error_high = (
        signals['signal'] == 'checkout_error_rate' and 
        signals['value'] > 25
    )

    if not checkout_error_high:
        return

    # 2. Check if Ticket Clusters already cover this
    # Look for "checkout" or "payment" in any detected cluster's stage or root cause
    ticket_coverage_exists = False
    for analysis in all_analyses:
        text_dump = (analysis['stage'] + analysis['root_cause']).lower()
        if 'checkout' in text_dump or 'payment' in text_dump:
            ticket_coverage_exists = True
            break
    
    # 3. PROACTIVE ALERT RULE
    # IF error is high AND no tickets exist yet -> Warn Support
    if not ticket_coverage_exists:
        print("\n" + "-"*40)
        print("PROACTIVE DETECTION")
        print(f"Detected elevated {signals['signal']} ({signals['value']}%) in last {signals['time_window']}.")
        print("No related support tickets reported yet.")
        print("Assumption: Issue detected before merchant reports.")
        print("Action: Notify support team and monitor closely.")
        print("-"*40)

def main():
    print("=== STARTING AGENTIC SUPPORT OPERATIONS MANAGER ===\n")

    # 1. OBSERVE (Tickets)
    tickets = observe.load_tickets()
    
    # 1b. OBSERVE (System Signals - NEW)
    signals = observe.load_system_signals() 

    # 2. REASON (Vectorize & Cluster)
    embeddings = embed.generate_embeddings(tickets)
    clusters = cluster.cluster_tickets(tickets, embeddings)

    all_cluster_analyses = []

    print("\n--- DETAILED CLUSTER REPORTS ---\n")

    # Iterate through ALL clusters
    for label, cluster_tickets in clusters.items():
        analysis = reason.analyze_cluster(label, cluster_tickets)
        decision = decide.determine_action(analysis)

        # (Existing print logic preserved...)
        print(f"[{analysis['cluster_name']}] ({analysis['ticket_count']} tickets)")
        print(f"  • Inferred Stage:  {analysis['stage']}")
        print(f"  • Root Cause:      {analysis['root_cause']}")
        print(f"  • Risk Level:      {decision['risk_level']}")
        print(f"  • ACTION:          {decision['recommended_action']}")
        print("-" * 40)
        
        all_cluster_analyses.append(analysis)

    # 5. GLOBAL ACT (Existing Ticket Alerts)
    generate_global_insight(all_cluster_analyses)

    # 6. PROACTIVE ACT (New Phase 2 Check)
    run_proactive_check(signals, all_cluster_analyses)

if __name__ == "__main__":
    main()