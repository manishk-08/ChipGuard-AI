# Implementation Plan: ChipGuard AI Codebase Cleanup and Completion

## Context
The project is an MVP for BOM risk and compliance intelligence. Based on the initial exploration, the backend appears well-structured with SQLAlchemy, FastAPI, and core services defined. The frontend exists but needs verification of its integration. The goal is to ensure the project is functional and stable.

## Current Status & Findings

### Backend
- **Functionality**: The core services (`BOMParser`, `RiskEngine`, `ComplianceScreener`) are defined and have basic tests.
- **Models/Database**: Models are defined in `backend/app/models/` and database interactions are in `backend/app/routes/`.
- **Gaps**:
    - Need to verify if the database migrations are fully functional.
    - Need to ensure all business logic in `services` is correctly exposed and handled in `routes`.
    - Need to run all tests to confirm stability.

### Frontend
- **Setup**: Next.js app exists, but needs thorough testing to ensure it correctly communicates with the backend APIs.

## Plan

### Phase 1: Verification
1.  **Run Backend Tests**: Confirm `pytest` passes for all services.
2.  **Run Backend Server**: Confirm `uvicorn` starts without errors.
3.  **Run Frontend Dev**: Confirm `npm run dev` starts and connects to the backend API.

### Phase 2: Implementation & Fixes
1.  **Address Test Failures**: If any tests fail, debug and fix the underlying logic.
2.  **Ensure API Consistency**: Check if `frontend/lib/api.ts` correctly points to the FastAPI backend.
3.  **Complete Missing Logic**: Implement any identified gaps in the API routes based on current model definitions.

### Phase 3: Final Verification
1.  Verify end-to-end BOM upload to risk report generation.
2.  Verify compliance screening.

## Verification
- Run full test suite: `pytest` and `npm test`.
- Manually trigger a BOM upload and monitor backend logs.
