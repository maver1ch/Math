"""
Module chọn solver phù hợp cho bài toán
"""
from config.llm_config import MODELS, DIFFICULTY_LEVELS
from core.tier2_solver.solvers.general_solver import GeneralSolver
from prompt_engineering.solving_prompts import get_solving_prompt

def select_solver(difficulty):
    """
    Chọn solver phù hợp dựa trên độ khó của bài toán
    
    Args:
        difficulty (int): Độ khó của bài toán (1-10)
        
    Returns:
        GeneralSolver: Solver phù hợp với độ khó
    """
    # Xác định mức độ khó
    if difficulty <= DIFFICULTY_LEVELS["easy"][1]:
        # Bài toán dễ
        model_config = MODELS["easy_solver"]
        thinking_budget = "low"
        solving_prompt = get_solving_prompt(difficulty)
    elif difficulty <= DIFFICULTY_LEVELS["medium"][1]:
        # Bài toán trung bình
        model_config = MODELS["medium_solver"]
        thinking_budget = "medium"
        solving_prompt = get_solving_prompt(difficulty)
    else:
        # Bài toán khó
        model_config = MODELS["hard_solver"]
        thinking_budget = "high"
        solving_prompt = get_solving_prompt(difficulty)
    
    # Tạo solver tương ứng
    solver = GeneralSolver(model_config, thinking_budget, solving_prompt)
    
    return solver