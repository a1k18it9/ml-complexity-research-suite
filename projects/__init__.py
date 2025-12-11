"""Projects package initialization."""

from typing import Dict, Type
from shared.base import BaseProject


def get_project(name: str) -> BaseProject:
    """Get project instance by name."""
    from projects.real_ram_deficit import RealRAMDeficitProject
    from projects.certified_ids_rl import CertifiedIDSProject
    from projects.stochastic_complexity import StochasticComplexityProject
    from projects.typological_constraint import TypologicalConstraintProject
    from projects.xai_pipeline import XAIPipelineProject
    from projects.fgc_real_ram import FGCRealRAMProject
    from projects.laplacian_solvers import LaplacianSolversProject
    from projects.advice_complexity import AdviceComplexityProject
    from projects.lp_type_optimization import LPTypeProject
    from projects.hpc_bottleneck import HPCBottleneckProject
    from projects.loss_landscapes import LossLandscapesProject
    from projects.pareto_safety import ParetoSafetyProject
    from projects.causal_counterfactual import CausalCounterfactualProject
    from projects.complexity_mapper import ComplexityMapperProject
    from projects.strategic_synthesis import StrategicSynthesisProject
    
    projects: Dict[str, Type[BaseProject]] = {
        "real_ram_deficit": RealRAMDeficitProject,
        "certified_ids_rl": CertifiedIDSProject,
        "stochastic_complexity": StochasticComplexityProject,
        "typological_constraint": TypologicalConstraintProject,
        "xai_pipeline": XAIPipelineProject,
        "fgc_real_ram": FGCRealRAMProject,
        "laplacian_solvers": LaplacianSolversProject,
        "advice_complexity": AdviceComplexityProject,
        "lp_type_optimization": LPTypeProject,
        "hpc_bottleneck": HPCBottleneckProject,
        "loss_landscapes": LossLandscapesProject,
        "pareto_safety": ParetoSafetyProject,
        "causal_counterfactual": CausalCounterfactualProject,
        "complexity_mapper": ComplexityMapperProject,
        "strategic_synthesis": StrategicSynthesisProject,
    }
    
    if name not in projects:
        raise ValueError(f"Unknown project: {name}. Available: {list(projects.keys())}")
    
    return projects[name]()


def list_projects() -> Dict[str, str]:
    """List all available projects."""
    return {
        "real_ram_deficit": "Real RAM Deficit Explorer",
        "certified_ids_rl": "Certified IDS for RL",
        "stochastic_complexity": "Stochastic Complexity Bounds",
        "typological_constraint": "Typological Constraint Complexity",
        "xai_pipeline": "XAI Pipeline Complexity",
        "fgc_real_ram": "FGC Real RAM Tools",
        "laplacian_solvers": "Laplacian Paradigm Solvers",
        "advice_complexity": "Advice Complexity for RL",
        "lp_type_optimization": "LP-Type Optimization Abstractions",
        "hpc_bottleneck": "Real-Time HPC Bottleneck Mitigation",
        "loss_landscapes": "Small Dimension Loss Landscapes",
        "pareto_safety": "Pareto Safety Under Advice",
        "causal_counterfactual": "Causal Counterfactual Bounds",
        "complexity_mapper": "ML Complexity Mapper",
        "strategic_synthesis": "D-INFK Strategic Synthesis",
    }
