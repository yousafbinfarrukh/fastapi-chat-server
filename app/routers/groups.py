from fastapi import APIRouter, Depends, HTTPException
from ..services.auth_service import get_current_user
from ..services.group_manager import group_manager

router = APIRouter(
    tags=['Groups']
)

@router.post("/create_group")
def create_group(group_name: str, current_user: str = Depends(get_current_user)):
    group_manager.create_group(group_name)
    return {"message": f"Group {group_name} created"}

@router.post("/join_group")
def join_group(group_name: str, current_user: str = Depends(get_current_user)):
    if group_name not in group_manager.groups:
        raise HTTPException(status_code=404, detail="Group not found")
    group_manager.add_user_to_group(group_name, current_user)
    return {"message": f"{current_user} joined group {group_name}"}

@router.post("/leave_group")
def leave_group(group_name: str, current_user: str = Depends(get_current_user)):
    if group_name not in group_manager.groups:
        raise HTTPException(status_code=404, detail="Group not found")
    group_manager.remove_user_from_group(group_name, current_user)
    return {"message": f"{current_user} left group {group_name}"}
