"""
Component hiển thị phân tích lỗ hổng kiến thức
"""
import streamlit as st

def render_knowledge_gaps(knowledge_analysis):
    """
    Hiển thị phân tích lỗ hổng kiến thức
    
    Args:
        knowledge_analysis (dict): Kết quả phân tích lỗ hổng kiến thức
    """
    st.subheader("📊 Phân tích lỗ hổng kiến thức")
    
    # Hiển thị đánh giá tổng quát
    if "overall_assessment" in knowledge_analysis:
        st.info(knowledge_analysis["overall_assessment"])
    
    # Hiển thị lỗ hổng kiến thức
    if "knowledge_gaps" in knowledge_analysis and knowledge_analysis["knowledge_gaps"]:
        st.markdown("### 🔍 Lỗ hổng kiến thức")
        
        for i, gap in enumerate(knowledge_analysis["knowledge_gaps"]):
            with st.expander(f"{gap['concept']} ({_get_confidence_level_text(gap['confidence_level'])})"):
                st.markdown(f"**Giải thích:** {gap['explanation']}")
                
                if "examples" in gap and gap["examples"]:
                    st.markdown("**Ví dụ:**")
                    for example in gap["examples"]:
                        st.markdown(f"- {example}")
    
    # Hiển thị điểm mạnh
    if "strengths" in knowledge_analysis and knowledge_analysis["strengths"]:
        st.markdown("### 💪 Điểm mạnh")
        
        for strength in knowledge_analysis["strengths"]:
            st.markdown(f"- **{strength['concept']}**: {strength['evidence']}")
    
    # Hiển thị đề xuất ôn tập
    if "study_recommendations" in knowledge_analysis and knowledge_analysis["study_recommendations"]:
        st.markdown("### 📚 Đề xuất ôn tập")
        
        for i, recommendation in enumerate(knowledge_analysis["study_recommendations"]):
            icon = _get_resource_icon(recommendation.get("resource_type", ""))
            st.markdown(f"{icon} **{recommendation['topic']}**: {recommendation['description']}")

def _get_confidence_level_text(level):
    """
    Chuyển đổi mức độ tự tin thành text tiếng Việt
    
    Args:
        level (str): Mức độ tự tin (low/medium/high)
        
    Returns:
        str: Text tiếng Việt tương ứng
    """
    if level == "low":
        return "Cần ôn tập nhiều"
    elif level == "medium":
        return "Cần củng cố thêm"
    elif level == "high":
        return "Cần ôn lại"
    else:
        return level

def _get_resource_icon(resource_type):
    """
    Lấy icon cho loại tài nguyên
    
    Args:
        resource_type (str): Loại tài nguyên
        
    Returns:
        str: Icon tương ứng
    """
    if resource_type == "video":
        return "🎬"
    elif resource_type == "book":
        return "📖"
    elif resource_type == "exercise":
        return "✏️"
    else:
        return "📌"