import Std.Tactic

namespace NewMathDiscovery.BlindnessRealization

/-- One target-false base state and one target-true state for each generator. -/
inductive State (J : Type) where
  | base
  | face (j : J)
  deriving DecidableEq

namespace State

def target {J : Type} : State J → Bool
  | .base => false
  | .face _ => true

/-- The base state reports `false`. A face state reports `false` exactly on
coordinates belonging to that face. -/
def observe {I J : Type} (F : J → I → Bool) (i : I) : State J → Bool
  | .base => false
  | .face j => !(F j i)

end State

/-- Two states are observationally indistinguishable to coalition `S`. -/
def AgreeOn {I X : Type} (S : I → Prop) (r : I → X → Bool)
    (x y : X) : Prop :=
  ∀ i, S i → r i x = r i y

/-- A coalition is target-blind if it cannot distinguish two states with
opposite Boolean targets. -/
def Blind {I X : Type} (S : I → Prop) (r : I → X → Bool)
    (q : X → Bool) : Prop :=
  ∃ x y, q x ≠ q y ∧ AgreeOn S r x y

/-- Exact realization theorem: the blind coalitions are precisely the subsets
of at least one Boolean generator. -/
theorem blind_iff_below_generator {I J : Type} (F : J → I → Bool)
    (S : I → Prop) :
    Blind S (State.observe F) State.target ↔
      ∃ j, ∀ i, S i → F j i = true := by
  constructor
  · rintro ⟨x, y, htarget, hagree⟩
    cases x with
    | base =>
        cases y with
        | base => exact False.elim (htarget rfl)
        | face j =>
            refine ⟨j, ?_⟩
            intro i hi
            have hobs := hagree i hi
            simp [State.observe] at hobs
            cases hF : F j i <;> simp [hF] at hobs ⊢
    | face j =>
        cases y with
        | base =>
            refine ⟨j, ?_⟩
            intro i hi
            have hobs := hagree i hi
            simp [State.observe] at hobs
            cases hF : F j i <;> simp [hF] at hobs ⊢
        | face k => exact False.elim (htarget rfl)
  · rintro ⟨j, hj⟩
    refine ⟨State.base, State.face j, by simp [State.target], ?_⟩
    intro i hi
    simp [State.observe, hj i hi]

/-- Downward closure is automatic, as a corollary of the exact realization. -/
theorem blind_downward {I J : Type} (F : J → I → Bool)
    {S T : I → Prop}
    (hsub : ∀ i, S i → T i)
    (hblind : Blind T (State.observe F) State.target) :
    Blind S (State.observe F) State.target := by
  rw [blind_iff_below_generator] at hblind ⊢
  obtain ⟨j, hj⟩ := hblind
  exact ⟨j, fun i hi => hj i (hsub i hi)⟩

#print axioms blind_iff_below_generator
#print axioms blind_downward

end NewMathDiscovery.BlindnessRealization
