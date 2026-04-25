"""
Episia tools wrapped as LangChain tools for the epidemiology agent.
Each tool maps a natural-language-friendly interface to episia's validated algorithms.
"""

import json
import traceback
from typing import Optional
from langchain_core.tools import tool


#  1. Sample Size · Risk Ratio (Cohort) 

@tool
def tool_sample_size_risk_ratio(
    risk_unexposed: float,
    risk_ratio: float,
    power: float = 0.80,
    alpha: float = 0.05,
    ratio_controls: int = 1,
) -> str:
    """
    Calculate sample size for a cohort study using the Risk Ratio method (Fleiss formula).
    
    Args:
        risk_unexposed: Baseline risk in unexposed group (proportion, e.g. 0.10 for 10%)
        risk_ratio: Expected risk ratio to detect (e.g. 2.0)
        power: Statistical power (default 0.80, range 0.70-0.95)
        alpha: Type I error / significance level (default 0.05)
        ratio_controls: Ratio of controls to cases (default 1)
    
    Returns:
        JSON string with n_cases, n_controls, n_total, R0, and interpretation.
    
    Example queries:
        - "How many subjects do I need to detect RR=2 with 80% power?"
        - "Sample size for cohort study, 10% baseline risk, RR=2.5"
        - "Taille d'échantillon pour détecter RR=3 avec puissance 90%"
    """
    try:
        from episia.stats.samplesize import sample_size_risk_ratio
        res = sample_size_risk_ratio(
            risk_unexposed=risk_unexposed,
            risk_ratio=risk_ratio,
            power=power,
            alpha=alpha,
            r=ratio_controls,
        )
        n_cases = int(res.n_per_group or res.n_cases or 0)
        n_ctrl  = int(n_cases * ratio_controls)
        n_total = n_cases + n_ctrl
        r1 = risk_unexposed * risk_ratio
        return json.dumps({
            "method": "Fleiss RR cohort formula (OpenEpi-validated)",
            "parameters": {
                "risk_unexposed": f"{risk_unexposed*100:.1f}%",
                "risk_exposed": f"{r1*100:.1f}%",
                "risk_ratio": risk_ratio,
                "power": f"{power*100:.0f}%",
                "alpha": alpha,
                "ratio_controls_cases": ratio_controls,
            },
            "results": {
                "n_exposed": n_cases,
                "n_unexposed": n_ctrl,
                "n_total": n_total,
            },
            "interpretation": (
                f"You need {n_cases} exposed and {n_ctrl} unexposed subjects "
                f"(total N={n_total}) to detect RR={risk_ratio} with "
                f"{power*100:.0f}% power and alpha={alpha}. "
                f"Baseline risk {risk_unexposed*100:.1f}% → exposed risk {r1*100:.1f}%."
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "traceback": traceback.format_exc()})


#  2. Sample Size · Odds Ratio (Case-Control) 

@tool
def tool_sample_size_odds_ratio(
    proportion_exposed_controls: float,
    odds_ratio: float,
    power: float = 0.80,
    alpha: float = 0.05,
) -> str:
    """
    Calculate sample size for a case-control study using the Odds Ratio method.
    
    Args:
        proportion_exposed_controls: Proportion exposed among controls (e.g. 0.30)
        odds_ratio: Expected odds ratio to detect (e.g. 2.5)
        power: Statistical power (default 0.80)
        alpha: Significance level (default 0.05)
    
    Returns:
        JSON with n_cases, n_controls, n_total, interpretation.
    
    Example queries:
        - "Case-control study, OR=2.5, 30% exposure in controls"
        - "Étude cas-témoin pour détecter OR=3, exposition dans les témoins 25%"
    """
    try:
        from episia.stats.samplesize import sample_size_odds_ratio
        res = sample_size_odds_ratio(
            proportion_exposed_controls=proportion_exposed_controls,
            odds_ratio=odds_ratio,
            power=power,
            alpha=alpha,
        )
        n_c = int(res.n_cases or 0)
        n_k = int(res.n_controls or 0)
        return json.dumps({
            "method": "Kelsey case-control formula (OpenEpi-validated)",
            "parameters": {
                "exposure_controls": f"{proportion_exposed_controls*100:.1f}%",
                "odds_ratio": odds_ratio,
                "power": f"{power*100:.0f}%",
                "alpha": alpha,
            },
            "results": {
                "n_cases": n_c,
                "n_controls": n_k,
                "n_total": n_c + n_k,
            },
            "interpretation": (
                f"You need {n_c} cases and {n_k} controls (total N={n_c+n_k}) "
                f"to detect OR={odds_ratio} with {power*100:.0f}% power."
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


#  3. Sample Size · Diagnostic Test 

@tool
def tool_sample_size_diagnostic(
    expected_sensitivity: float,
    expected_specificity: float,
    precision: float = 0.07,
    prevalence: float = 0.20,
) -> str:
    """
    Calculate sample size for a diagnostic test evaluation study.
    
    Args:
        expected_sensitivity: Expected sensitivity (proportion, e.g. 0.85)
        expected_specificity: Expected specificity (proportion, e.g. 0.92)
        precision: Half-width of 95% CI (default 0.07 = ±7%)
        prevalence: Disease prevalence in study population (e.g. 0.20)
    
    Returns:
        JSON with n_diseased, n_non_diseased, n_total.
    
    Example queries:
        - "Sample size to validate an RDT with expected sensitivity 85%, specificity 92%"
        - "Combien de sujets pour évaluer un TDR paludisme, sensibilité attendue 90%?"
    """
    try:
        from episia.stats.samplesize import sample_size_sensitivity_specificity
        res = sample_size_sensitivity_specificity(
            expected_sens=expected_sensitivity,
            expected_spec=expected_specificity,
            precision=precision,
            prevalence=prevalence,
        )
        n_pos = int(res.n_cases or 0)
        n_neg = int(res.n_controls or 0)
        return json.dumps({
            "method": "Buderer diagnostic accuracy formula",
            "parameters": {
                "expected_sensitivity": f"{expected_sensitivity*100:.0f}%",
                "expected_specificity": f"{expected_specificity*100:.0f}%",
                "precision": f"±{precision*100:.0f}%",
                "prevalence": f"{prevalence*100:.0f}%",
            },
            "results": {
                "n_disease_positive": n_pos,
                "n_disease_negative": n_neg,
                "n_total": n_pos + n_neg,
            },
            "interpretation": (
                f"You need {n_pos} disease-positive and {n_neg} disease-negative subjects "
                f"(total N={n_pos+n_neg}) to estimate sensitivity={expected_sensitivity*100:.0f}% "
                f"and specificity={expected_specificity*100:.0f}% with precision ±{precision*100:.0f}%."
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


#  4. Sample Size · Single Proportion 

@tool
def tool_sample_size_proportion(
    expected_proportion: float,
    precision: float = 0.05,
    alpha: float = 0.05,
    design_effect: float = 1.0,
) -> str:
    """
    Calculate sample size for a single proportion survey (e.g. seroprevalence, coverage).
    
    Args:
        expected_proportion: Expected proportion (e.g. 0.30 for 30%)
        precision: Acceptable margin of error (default 0.05 = ±5%)
        alpha: Significance level (default 0.05)
        design_effect: DEFF for cluster sampling (default 1.0 = simple random)
    
    Returns:
        JSON with required sample size, accounting for design effect.
    
    Example queries:
        - "Survey sample size to estimate 30% malaria prevalence with ±5% precision"
        - "Enquête SMART, proportion attendue 25%, sondage en grappes DEFF=1.5"
        - "Vaccination coverage survey, expected 70%, precision ±8%"
    """
    try:
        from episia.stats.samplesize import sample_size_single_proportion
        res = sample_size_single_proportion(
            expected_proportion=expected_proportion,
            precision=precision,
            alpha=alpha,
            design_effect=design_effect,
        )
        n = int(res.n_per_group or res.n_total or 0)
        return json.dumps({
            "method": "Cochran single proportion formula",
            "parameters": {
                "expected_proportion": f"{expected_proportion*100:.0f}%",
                "precision": f"±{precision*100:.0f}%",
                "alpha": alpha,
                "design_effect": design_effect,
            },
            "results": {
                "n_required": n,
                "note": "Add 10-15% for non-response" if design_effect == 1.0 else f"DEFF={design_effect} already applied",
            },
            "interpretation": (
                f"You need N={n} subjects to estimate a proportion of "
                f"{expected_proportion*100:.0f}% with precision ±{precision*100:.0f}% "
                f"(alpha={alpha}, DEFF={design_effect})."
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


#  5. Vaccine Efficacy 

@tool
def tool_vaccine_efficacy(
    cases_vaccinated: int,
    total_vaccinated: int,
    cases_unvaccinated: int,
    total_unvaccinated: int,
    study_type: str = "cohort",
) -> str:
    """
    Compute vaccine efficacy (VE) from cohort or case-control study data.
    VE = (1 - Risk Ratio) × 100%.
    
    Args:
        cases_vaccinated: Number of cases in vaccinated group
        total_vaccinated: Total vaccinated subjects (cases + non-cases)
        cases_unvaccinated: Number of cases in unvaccinated group
        total_unvaccinated: Total unvaccinated subjects
        study_type: "cohort" (default) or "case_control"
    
    Returns:
        JSON with VE, RR, 95% CI, p-value, risk rates, interpretation.
    
    Example queries:
        - "Vaccine efficacy: 12 cases among 3000 vaccinated, 87 cases among 3000 unvaccinated"
        - "Calcule l'efficacité vaccinale MenAfriVac: 5 cas sur 1500 vaccinés, 42 cas sur 1500 non vaccinés"
        - "VE with 95% CI for these 2x2 table data"
    """
    try:
        from episia.stats.contingency import risk_ratio, odds_ratio
        
        non_cases_vacc  = total_vaccinated - cases_vaccinated
        non_cases_unvacc = total_unvaccinated - cases_unvaccinated
        
        rr  = risk_ratio(a=cases_vaccinated, b=non_cases_vacc,
                          c=cases_unvaccinated, d=non_cases_unvacc)
        
        ve     = (1 - rr.estimate) * 100
        ve_lo  = (1 - rr.ci_upper) * 100
        ve_hi  = (1 - rr.ci_lower) * 100
        r_vacc = cases_vaccinated / total_vaccinated * 1000
        r_unv  = cases_unvaccinated / total_unvaccinated * 1000
        
        # p-value formatting
        p = rr.p_value
        p_str = "<0.0001" if p < 0.0001 else f"{p:.4f}" if p < 0.001 else f"{p:.3f}"
        
        # Interpretation
        if ve >= 80 and p < 0.05:
            interp = f"HIGH vaccine efficacy ({ve:.1f}%), statistically significant."
        elif ve >= 50 and p < 0.05:
            interp = f"MODERATE vaccine efficacy ({ve:.1f}%), statistically significant. Consider improving coverage."
        elif ve >= 50 and p >= 0.05:
            interp = f"Moderate apparent VE ({ve:.1f}%) but NOT statistically significant (p={p_str}). Increase study power."
        elif ve < 0:
            interp = f"NEGATIVE VE ({ve:.1f}%): vaccinated have MORE risk than unvaccinated. Investigate cold chain failure, selection bias, or waning immunity."
        else:
            interp = f"Low vaccine efficacy ({ve:.1f}%). Review vaccine lot, cold chain, and coverage strategy."
        
        return json.dumps({
            "method": "Vaccine Efficacy = 1 - Risk Ratio (OpenEpi-validated)",
            "contingency_table": {
                "cases_vaccinated": cases_vaccinated,
                "non_cases_vaccinated": non_cases_vacc,
                "cases_unvaccinated": cases_unvaccinated,
                "non_cases_unvaccinated": non_cases_unvacc,
            },
            "results": {
                "vaccine_efficacy": f"{ve:.1f}%",
                "VE_95CI": f"[{ve_lo:.1f}% – {ve_hi:.1f}%]",
                "risk_ratio": round(rr.estimate, 4),
                "RR_95CI": f"[{rr.ci_lower:.4f} – {rr.ci_upper:.4f}]",
                "p_value": p_str,
                "risk_vaccinated_per_1000": round(r_vacc, 2),
                "risk_unvaccinated_per_1000": round(r_unv, 2),
                "ARR_per_1000": round(r_unv - r_vacc, 2),
                "NNV": round(1000 / max(r_unv - r_vacc, 0.001), 0),
            },
            "interpretation": interp
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "traceback": traceback.format_exc()})


#  6. Diagnostic Test Evaluation 

@tool
def tool_diagnostic_test(
    true_positives: int,
    false_positives: int,
    false_negatives: int,
    true_negatives: int,
    prevalence_for_ppv: float = 0.20,
) -> str:
    """
    Evaluate a diagnostic test (RDT, PCR, etc.) against a gold standard.
    Computes sensitivity, specificity, LR+, LR-, PPV, NPV.
    
    Args:
        true_positives: Test+, Disease+ 
        false_positives: Test+, Disease- (false alarms)
        false_negatives: Test-, Disease+ (missed cases)
        true_negatives: Test-, Disease-
        prevalence_for_ppv: Local disease prevalence for PPV/NPV calculation (default 0.20)
    
    Returns:
        JSON with full diagnostic performance metrics and clinical interpretation.
    
    Example queries:
        - "Evaluate malaria RDT: 142 TP, 18 FP, 23 FN, 317 TN"
        - "Performance TDR paludisme : 120 VP, 8 FP, 15 FN, 280 VN, prévalence locale 35%"
        - "Should we use this RDT at 15% malaria prevalence?"
    """
    try:
        from episia.stats.diagnostic import diagnostic_test_2x2, predictive_values_from_sens_spec
        
        d = diagnostic_test_2x2(tp=true_positives, fp=false_positives,
                                 fn=false_negatives, tn=true_negatives)
        
        ppv, npv = predictive_values_from_sens_spec(d.sensitivity, d.specificity, prevalence_for_ppv)
        
        total = true_positives + false_positives + false_negatives + true_negatives
        acc   = (true_positives + true_negatives) / total * 100
        
        # WHO RDT threshold: sensitivity ≥95%, specificity ≥90% for malaria
        who_flag = []
        if d.sensitivity < 0.95:
            who_flag.append(f"⚠️ Sensitivity {d.sensitivity*100:.1f}% below WHO malaria RDT threshold (95%)")
        if d.specificity < 0.90:
            who_flag.append(f"⚠️ Specificity {d.specificity*100:.1f}% below WHO malaria RDT threshold (90%)")
        if not who_flag:
            who_flag.append("✅ Meets WHO minimum performance thresholds for malaria RDTs")
        
        return json.dumps({
            "method": "Diagnostic 2x2 table (OpenEpi-validated)",
            "parameters": {
                "prevalence_used_for_PPV_NPV": f"{prevalence_for_ppv*100:.0f}%"
            },
            "performance_metrics": {
                "sensitivity": f"{d.sensitivity*100:.1f}%",
                "specificity": f"{d.specificity*100:.1f}%",
                "accuracy": f"{acc:.1f}%",
                "LR_positive": round(d.lr_positive, 2),
                "LR_negative": round(d.lr_negative, 3),
                "PPV_at_given_prevalence": f"{ppv*100:.1f}%",
                "NPV_at_given_prevalence": f"{npv*100:.1f}%",
                "Youden_index": round(d.sensitivity + d.specificity - 1, 3),
            },
            "who_assessment": who_flag,
            "operational_impact_per_100_patients": {
                "expected_true_cases": int(100 * prevalence_for_ppv),
                "estimated_missed_cases": int(100 * prevalence_for_ppv * (1 - d.sensitivity)),
                "estimated_false_alarms": int(100 * (1 - prevalence_for_ppv) * (1 - d.specificity)),
            },
            "interpretation": (
                f"Sensitivity={d.sensitivity*100:.1f}%, Specificity={d.specificity*100:.1f}%. "
                f"At {prevalence_for_ppv*100:.0f}% prevalence: PPV={ppv*100:.1f}% (probability test+ is truly positive), "
                f"NPV={npv*100:.1f}% (probability test- is truly negative). "
                f"LR+={d.lr_positive:.1f} (good if >10), LR-={d.lr_negative:.3f} (good if <0.1)."
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


#  7. SEIR Outbreak Simulation 

@tool
def tool_seir_simulation(
    population: int,
    initial_infected: int = 5,
    initial_exposed: int = 20,
    beta: float = 0.42,
    sigma: float = 0.25,
    gamma: float = 0.143,
    vaccine_coverage: float = 0.0,
    days: int = 120,
) -> str:
    """
    Run a SEIR compartmental model to simulate an epidemic outbreak.
    Compares baseline vs. vaccination scenario.
    
    Args:
        population: Total susceptible population
        initial_infected: Number of initial infected cases (default 5)
        initial_exposed: Number of initial exposed (default 20)
        beta: Transmission rate (default 0.42, typical for meningitis)
        sigma: Inverse of incubation period (default 0.25 = 4-day incubation)
        gamma: Recovery rate (default 0.143 = 7-day infectious period)
        vaccine_coverage: Proportion vaccinated (0.0 to 1.0, default 0.0 = no vaccine)
        days: Simulation duration in days (default 120)
    
    Returns:
        JSON with peak infected, peak day, final attack rate, R0, comparison.
    
    Example queries:
        - "Simulate meningitis outbreak in Kaya district, population 350000"
        - "SEIR model for Burkina Faso district, what happens with 60% vaccination coverage?"
        - "Modélise une épidémie de méningite, R0=3, population 200000"
    """
    try:
        from episia.models import SEIRModel
        from episia.models.parameters import SEIRParameters
        import numpy as np
        
        # Baseline (no vaccine)
        params_base = SEIRParameters(
            N=population, I0=initial_infected, E0=initial_exposed,
            beta=beta, sigma=sigma, gamma=gamma, t_span=(0, days)
        )
        result_base = SEIRModel(params_base).run()
        I_base = result_base.compartments["I"]
        R_base = result_base.compartments.get("R", [0])
        
        peak_I   = float(np.max(I_base))
        peak_day = int(np.argmax(I_base))
        final_R  = float(R_base[-1])
        attack_rate = final_R / population * 100
        R0 = beta / gamma
        
        # With vaccination
        N_eff = int(population * (1 - vaccine_coverage))
        params_vax = SEIRParameters(
            N=N_eff, I0=initial_infected, E0=initial_exposed,
            beta=beta, sigma=sigma, gamma=gamma, t_span=(0, days)
        )
        result_vax = SEIRModel(params_vax).run()
        I_vax      = result_vax.compartments["I"]
        R_vax      = result_vax.compartments.get("R", [0])
        peak_I_vax = float(np.max(I_vax))
        ar_vax     = float(R_vax[-1]) / population * 100
        
        # Herd immunity threshold
        herd_threshold = (1 - 1/R0) * 100 if R0 > 1 else 0
        
        return json.dumps({
            "method": "SEIR compartmental model (Euler integration)",
            "parameters": {
                "population": population,
                "R0": round(R0, 2),
                "beta": beta, "sigma": sigma, "gamma": gamma,
                "mean_incubation_days": round(1/sigma, 1),
                "mean_infectious_days": round(1/gamma, 1),
                "herd_immunity_threshold": f"{herd_threshold:.1f}%",
            },
            "scenario_no_vaccine": {
                "peak_infected": int(peak_I),
                "peak_day": peak_day,
                "final_attack_rate": f"{attack_rate:.1f}%",
                "total_cases_estimate": int(final_R),
            },
            "scenario_with_vaccination": {
                "coverage": f"{vaccine_coverage*100:.0f}%",
                "peak_infected": int(peak_I_vax),
                "final_attack_rate": f"{ar_vax:.1f}%",
                "cases_averted": int(final_R - float(R_vax[-1])),
                "reduction": f"{(1 - ar_vax/max(attack_rate, 0.001))*100:.0f}%",
            } if vaccine_coverage > 0 else "No vaccination scenario requested",
            "interpretation": (
                f"R0={R0:.2f} ({'epidemic will grow' if R0 > 1 else 'epidemic will fade'}). "
                f"Without intervention: peak {int(peak_I)} infected on day {peak_day}, "
                f"final attack rate {attack_rate:.1f}%. "
                f"Herd immunity requires ≥{herd_threshold:.0f}% coverage."
                + (f" With {vaccine_coverage*100:.0f}% vaccination: peak reduced to {int(peak_I_vax)} ({(1-peak_I_vax/max(peak_I,1))*100:.0f}% reduction)." if vaccine_coverage > 0 else "")
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "traceback": traceback.format_exc()})


#  8. HIV Cascade Analysis 

@tool
def tool_hiv_cascade(
    plhiv: int,
    pct_know_status: float,
    pct_on_art: float,
    pct_virally_suppressed: float,
    target_1: float = 90.0,
    target_2: float = 90.0,
    target_3: float = 90.0,
) -> str:
    """
    Analyse the HIV treatment cascade and gap to UNAIDS 90-90-90 targets.
    
    Args:
        plhiv: Estimated people living with HIV (PLHIV)
        pct_know_status: % of PLHIV who know their status (1st 90)
        pct_on_art: % of those who know status who are on ART (2nd 90)
        pct_virally_suppressed: % of those on ART who are virally suppressed (3rd 90)
        target_1: Target for 1st 90 (default 90%)
        target_2: Target for 2nd 90 (default 90%)
        target_3: Target for 3rd 90 (default 90%)
    
    Returns:
        JSON with cascade numbers, gaps, overall suppression, recommendations.
    
    Example queries:
        - "HIV cascade Burkina Faso: 110000 PLHIV, 66% know status, 79% on ART, 88% suppressed"
        - "Analyse la cascade VIH Ouagadougou, 24000 PVVIH, 72-83-91"
        - "Gap to 90-90-90 for Ghana: 350000 PLHIV, current 79-85-93"
    """
    try:
        n_know = int(plhiv * pct_know_status / 100)
        n_art  = int(n_know * pct_on_art / 100)
        n_supp = int(n_art * pct_virally_suppressed / 100)
        
        overall_suppression = n_supp / plhiv * 100
        
        # Targets
        t_know = int(plhiv * target_1 / 100)
        t_art  = int(t_know * target_2 / 100)
        t_supp = int(t_art * target_3 / 100)
        
        # Gaps
        gap_know = t_know - n_know
        gap_art  = t_art - n_art
        gap_supp = t_supp - n_supp
        
        # 90-90-90 overall = 0.9*0.9*0.9 = 72.9% suppressed of all PLHIV
        target_overall = (target_1/100) * (target_2/100) * (target_3/100) * 100
        
        return json.dumps({
            "method": "UNAIDS HIV Treatment Cascade Analysis",
            "input_cascade": {
                "PLHIV": plhiv,
                "knowing_status": f"{pct_know_status}% → {n_know:,} people",
                "on_ART": f"{pct_on_art}% of those → {n_art:,} people",
                "virally_suppressed": f"{pct_virally_suppressed}% of those → {n_supp:,} people",
            },
            "overall_viral_suppression": f"{overall_suppression:.1f}% of all PLHIV",
            "target_cascade": {
                "target_knowing_status": f"{target_1}% → {t_know:,} people",
                "target_on_ART": f"{target_2}% → {t_art:,} people",
                "target_suppressed": f"{target_3}% → {t_supp:,} people",
                "target_overall_suppression": f"{target_overall:.1f}% of all PLHIV",
            },
            "gaps_to_target": {
                "additional_people_to_diagnose": gap_know,
                "additional_people_to_initiate_ART": gap_art,
                "additional_people_to_reach_suppression": gap_supp,
            },
            "unmet_need": {
                "undiagnosed": plhiv - n_know,
                "diagnosed_not_on_ART": n_know - n_art,
                "on_ART_not_suppressed": n_art - n_supp,
            },
            "interpretation": (
                f"Current cascade: {pct_know_status}–{pct_on_art}–{pct_virally_suppressed}. "
                f"Overall viral suppression: {overall_suppression:.1f}% of all PLHIV "
                f"(target {target_overall:.1f}%). "
                f"To reach {target_1:.0f}-{target_2:.0f}-{target_3:.0f} targets: "
                f"need to diagnose {gap_know:,} more, initiate ART for {gap_art:,} more, "
                f"achieve suppression for {gap_supp:,} more people."
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


#  9. MUAC Malnutrition Screening 

@tool
def tool_muac_analysis(
    n_screened: int,
    n_sam: int,
    n_mam: int,
    population_under5: Optional[int] = None,
    itfc_capacity: int = 25,
    otp_capacity: int = 120,
    tsfp_capacity: int = 300,
) -> str:
    """
    Analyze MUAC screening results and assess acute malnutrition burden.
    Classifies GAM situation and compares caseload to programme capacity.
    
    Args:
        n_screened: Number of children screened
        n_sam: Number with SAM (MUAC <115mm)
        n_mam: Number with MAM (MUAC 115–125mm)
        population_under5: Total under-5 population (optional, for coverage)
        itfc_capacity: ITFC (inpatient) bed capacity (default 25)
        otp_capacity: OTP (outpatient SAM) slots (default 120)
        tsfp_capacity: TSFP (MAM) programme slots (default 300)
    
    Returns:
        JSON with prevalences, GAM status, programme capacity analysis.
    
    Example queries:
        - "MUAC results Titao district: 8125 screened, 450 SAM, 820 MAM, OTP capacity 120"
        - "Analyse dépistage MUAC: 5000 enfants, 380 MAS, 650 MAM"
        - "GAM situation in Dori district: 6000 screened, 8% SAM, 15% MAM"
    """
    try:
        sam_prev = n_sam / n_screened * 100
        mam_prev = n_mam / n_screened * 100
        gam_prev = (n_sam + n_mam) / n_screened * 100
        
        # WHO classification
        if gam_prev >= 15:
            gam_status = "EMERGENCY (≥15%)"
            action = "Immediate scale-up required. Activate emergency nutrition response."
        elif gam_prev >= 10:
            gam_status = "SERIOUS (10–14.9%)"
            action = "Urgent programme strengthening. Alert nutrition cluster."
        else:
            gam_status = "ACCEPTABLE (<10%)"
            action = "Maintain surveillance. Monitor seasonal trends."
        
        # Caseload split (15% inpatient, 85% outpatient)
        itfc_load = int(n_sam * 0.15)
        otp_load  = int(n_sam * 0.85)
        tsfp_load = n_mam
        
        capacity_analysis = {}
        for prog, load, cap in [("ITFC", itfc_load, itfc_capacity),
                                  ("OTP", otp_load, otp_capacity),
                                  ("TSFP", tsfp_load, tsfp_capacity)]:
            ratio = load / max(cap, 1) * 100
            capacity_analysis[prog] = {
                "caseload": load,
                "capacity": cap,
                "utilization": f"{ratio:.0f}%",
                "status": "OVERCAPACITY" if ratio > 100 else "NEAR_SATURATION" if ratio > 80 else "ADEQUATE",
                "gap": max(load - cap, 0),
            }
        
        # RUTF/CSB cost estimate
        monthly_cost = itfc_load * 85 + otp_load * 45 + tsfp_load * 18
        
        screening_coverage = (n_screened / population_under5 * 100) if population_under5 else None
        
        return json.dumps({
            "method": "WHO MUAC acute malnutrition classification",
            "screening": {
                "n_screened": n_screened,
                "coverage": f"{screening_coverage:.0f}%" if screening_coverage else "Unknown",
            },
            "prevalences": {
                "SAM": f"{sam_prev:.1f}% ({n_sam} children)",
                "MAM": f"{mam_prev:.1f}% ({n_mam} children)",
                "GAM": f"{gam_prev:.1f}% ({n_sam + n_mam} children)",
            },
            "who_classification": gam_status,
            "recommended_action": action,
            "programme_capacity": capacity_analysis,
            "estimated_monthly_rutf_cost_usd": monthly_cost,
            "interpretation": (
                f"GAM={gam_prev:.1f}% → {gam_status}. "
                f"SAM: {sam_prev:.1f}% ({n_sam} children), MAM: {mam_prev:.1f}% ({n_mam} children). "
                + "".join([
                    f"{p}: {v['status']} ({v['utilization']} utilization{', ' + str(v['gap']) + ' children above capacity' if v['gap'] > 0 else ''}). "
                    for p, v in capacity_analysis.items()
                ])
                + f"Estimated monthly RUTF/CSB++ cost: ${monthly_cost:,}."
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


#  10. Alert Detection 

@tool
def tool_epidemic_alert(
    weekly_cases: list,
    population: int,
    threshold_cases_per_week: int = 15,
    disease: str = "meningitis",
) -> str:
    """
    Analyze weekly surveillance data and detect epidemic alerts.
    
    Args:
        weekly_cases: List of weekly case counts (e.g. [2, 3, 5, 12, 28, 45, ...])
        population: District population
        threshold_cases_per_week: Epidemic threshold (default 15 for meningitis belt)
        disease: Disease name for context (default "meningitis")
    
    Returns:
        JSON with alert weeks, attack rate, epidemic status, recommendations.
    
    Example queries:
        - "Alert analysis: weekly cases [2,3,5,12,28,45,60,42,18,8,3], threshold 15, pop 350000"
        - "Is this meningitis data showing an epidemic? cases: [1,2,4,18,35,52,41,20,6,2]"
        - "Détecte les semaines épidémiques dans cette série: [3,2,5,4,20,45,62,38,12,5]"
    """
    try:
        import numpy as np
        
        cases = np.array(weekly_cases)
        n_weeks = len(cases)
        total_cases = int(cases.sum())
        peak_cases = int(cases.max())
        peak_week  = int(np.argmax(cases)) + 1
        attack_rate = total_cases / population * 100_000
        
        # Epidemic weeks
        epidemic_weeks = [i+1 for i, c in enumerate(cases) if c >= threshold_cases_per_week]
        
        # Z-score alerts
        mean_c = cases.mean()
        std_c  = cases.std()
        zscore_alerts = []
        if std_c > 0:
            zscore_alerts = [i+1 for i, c in enumerate(cases) 
                              if (c - mean_c) / std_c > 2.0]
        
        # Moving average
        ma = np.convolve(cases, np.ones(3)/3, mode='valid').tolist()
        
        # Status
        if len(epidemic_weeks) >= 3:
            status = "CONFIRMED EPIDEMIC"
            action = f"Activate epidemic response. Notify district health team. Consider mass vaccination if {disease}."
        elif len(epidemic_weeks) >= 1:
            status = "EPIDEMIC ALERT"
            action = "Investigate immediately. Collect samples. Prepare response plan."
        elif len(zscore_alerts) >= 1:
            status = "STATISTICAL WARNING"
            action = "Monitor closely. Verify data quality. Investigate potential source."
        else:
            status = "ENDEMIC / BACKGROUND"
            action = "Continue routine surveillance."
        
        return json.dumps({
            "method": "WHO epidemic alert detection (threshold + Z-score)",
            "disease": disease,
            "surveillance_period": f"{n_weeks} weeks",
            "summary": {
                "total_cases": total_cases,
                "peak_cases_per_week": peak_cases,
                "peak_week": peak_week,
                "attack_rate_per_100k": round(attack_rate, 1),
                "weeks_above_threshold": len(epidemic_weeks),
                "epidemic_threshold": threshold_cases_per_week,
            },
            "alerts": {
                "epidemic_weeks": epidemic_weeks,
                "zscore_alert_weeks": zscore_alerts,
            },
            "status": status,
            "recommended_action": action,
            "interpretation": (
                f"Over {n_weeks} weeks: {total_cases} total cases, peak {peak_cases} in week {peak_week}. "
                f"Attack rate {attack_rate:.1f}/100,000. "
                f"{len(epidemic_weeks)} epidemic weeks (≥{threshold_cases_per_week} cases/week). "
                f"Status: {status}. {action}"
            )
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


#  All tools list 

ALL_TOOLS = [
    tool_sample_size_risk_ratio,
    tool_sample_size_odds_ratio,
    tool_sample_size_diagnostic,
    tool_sample_size_proportion,
    tool_vaccine_efficacy,
    tool_diagnostic_test,
    tool_seir_simulation,
    tool_hiv_cascade,
    tool_muac_analysis,
    tool_epidemic_alert,
]
