import Std.Tactic

/-!
# Linear blindness as a common-kernel obstruction

This file isolates the exact algebraic obstruction behind target blindness.
It uses only subtraction-preserving maps, so it does not require Mathlib's
linear-algebra hierarchy.  Every linear map between modules is an instance of
this interface after forgetting scalar multiplication.
-/

namespace NewMathDiscovery.LinearBlindness

/-- A family of subtraction-preserving observations and one
subtraction-preserving target.  `sub_eq_zero_iff` records the only cancellation
law about the codomain needed below.

The interface is deliberately weaker than a module: ordinary linear
functionals satisfy all of these fields. -/
structure System (Index State Value : Type) where
  zeroState : State
  subState : State → State → State
  zeroValue : Value
  subValue : Value → Value → Value
  observe : Index → State → Value
  target : State → Value
  observe_zero : ∀ i, observe i zeroState = zeroValue
  target_zero : target zeroState = zeroValue
  observe_sub : ∀ i x y,
    observe i (subState x y) = subValue (observe i x) (observe i y)
  target_sub : ∀ x y,
    target (subState x y) = subValue (target x) (target y)
  sub_eq_zero_iff : ∀ a b, subValue a b = zeroValue ↔ a = b

/-- The selected observations cannot distinguish two states on which the
target differs. -/
def PairBlind {Index State Value : Type} (system : System Index State Value)
    (selected : Index → Prop) : Prop :=
  ∃ x y,
    system.target x ≠ system.target y ∧
      ∀ i, selected i → system.observe i x = system.observe i y

/-- A direction lies in the common kernel of the selected observations. -/
def InObservationKernel {Index State Value : Type}
    (system : System Index State Value) (selected : Index → Prop)
    (direction : State) : Prop :=
  ∀ i, selected i → system.observe i direction = system.zeroValue

/-- A common-kernel direction on which the target is nonzero. -/
def KernelWitness {Index State Value : Type}
    (system : System Index State Value) (selected : Index → Prop) : Prop :=
  ∃ direction,
    InObservationKernel system selected direction ∧
      system.target direction ≠ system.zeroValue

/-- Exact difference-witness characterization: pairwise target blindness is
equivalent to a direction in every selected observation kernel but outside the
target kernel. -/
theorem pairBlind_iff_kernelWitness {Index State Value : Type}
    (system : System Index State Value) (selected : Index → Prop) :
    PairBlind system selected ↔ KernelWitness system selected := by
  constructor
  · rintro ⟨x, y, htarget, hagree⟩
    refine ⟨system.subState x y, ?_, ?_⟩
    · intro i hi
      rw [system.observe_sub]
      exact (system.sub_eq_zero_iff _ _).2 (hagree i hi)
    · rw [system.target_sub]
      intro hzero
      exact htarget ((system.sub_eq_zero_iff _ _).1 hzero)
  · rintro ⟨direction, hkernel, htarget⟩
    refine ⟨direction, system.zeroState, ?_, ?_⟩
    · simpa only [system.target_zero] using htarget
    · intro i hi
      simpa only [system.observe_zero] using hkernel i hi

/-- The selected observations determine the target on all pairs of states. -/
def DeterminesTarget {Index State Value : Type}
    (system : System Index State Value) (selected : Index → Prop) : Prop :=
  ∀ x y,
    (∀ i, selected i → system.observe i x = system.observe i y) →
      system.target x = system.target y

/-- Exact positive form of the criterion: the selected observations determine
the target precisely when their common kernel is contained in the target
kernel. -/
theorem determinesTarget_iff_kernel_inclusion {Index State Value : Type}
    (system : System Index State Value) (selected : Index → Prop) :
    DeterminesTarget system selected ↔
      ∀ direction,
        InObservationKernel system selected direction →
          system.target direction = system.zeroValue := by
  constructor
  · intro hdetermines direction hkernel
    have hagree : ∀ i, selected i →
        system.observe i direction = system.observe i system.zeroState := by
      intro i hi
      rw [system.observe_zero]
      exact hkernel i hi
    have htarget := hdetermines direction system.zeroState hagree
    simpa only [system.target_zero] using htarget
  · intro hinclusion x y hagree
    have hkernel : InObservationKernel system selected
        (system.subState x y) := by
      intro i hi
      rw [system.observe_sub]
      exact (system.sub_eq_zero_iff _ _).2 (hagree i hi)
    have htargetZero := hinclusion (system.subState x y) hkernel
    rw [system.target_sub] at htargetZero
    exact (system.sub_eq_zero_iff _ _).1 htargetZero

/-- Removing observations cannot destroy an existing blindness witness. -/
theorem pairBlind_downward {Index State Value : Type}
    (system : System Index State Value) {smaller larger : Index → Prop}
    (hsubset : ∀ i, smaller i → larger i)
    (hblind : PairBlind system larger) :
    PairBlind system smaller := by
  obtain ⟨x, y, htarget, hagree⟩ := hblind
  exact ⟨x, y, htarget, fun i hi => hagree i (hsubset i hi)⟩

/-!
## A rank-two degeneration that defeats a naive robustness score

The covectors below are

* target row `q = (1, 0)`;
* sensor row `r_n = (1, n + 1)`.

Every pair of distinct rows has nonzero determinant, so every finite prefix
represents the same uniform rank-two matroid.  Nevertheless, the kernel of
`r_n` contains `(n + 1, -1)`.  After fixing the second coordinate to `-1`,
the target coordinate is unbounded.  Projectively, these blind directions
approach the target axis while the represented matroid stays unchanged.

This exact integer family is a falsifier for robustness objectives that reward
only the target's size on one blind kernel and ignore margins to *all* matroid
incidences.  It deliberately makes no claim about a repaired condition number.
-/
namespace RankTwoInstability

def targetRow : Int × Int := (1, 0)

def sensorRow (n : Nat) : Int × Int := (1, Int.ofNat n + 1)

def determinant (a b : Int × Int) : Int :=
  a.1 * b.2 - a.2 * b.1

def target (x : Int × Int) : Int := x.1

def observe (n : Nat) (x : Int × Int) : Int :=
  x.1 + (Int.ofNat n + 1) * x.2

def witness (n : Nat) : Int × Int :=
  (Int.ofNat n + 1, -1)

theorem target_sensor_minor (n : Nat) :
    determinant targetRow (sensorRow n) = Int.ofNat n + 1 := by
  simp [determinant, targetRow, sensorRow]

theorem distinct_sensor_minor {m n : Nat} (hne : m ≠ n) :
    determinant (sensorRow m) (sensorRow n) ≠ 0 := by
  simp [determinant, sensorRow]
  omega

theorem witness_in_sensor_kernel (n : Nat) :
    observe n (witness n) = 0 := by
  simp [observe, witness]
  omega

theorem target_nonzero_on_witness (n : Nat) :
    target (witness n) ≠ 0 := by
  simp [target, witness]
  omega

theorem unbounded_target_on_gauge_fixed_kernel (bound : Nat) :
    ∃ n direction,
      observe n direction = 0 ∧
      direction.2 = -1 ∧
      target direction > Int.ofNat bound := by
  refine ⟨bound, witness bound, witness_in_sensor_kernel bound, rfl, ?_⟩
  simp [target, witness]
  omega

#print axioms target_sensor_minor
#print axioms distinct_sensor_minor
#print axioms witness_in_sensor_kernel
#print axioms target_nonzero_on_witness
#print axioms unbounded_target_on_gauge_fixed_kernel

end RankTwoInstability

#print axioms pairBlind_iff_kernelWitness
#print axioms determinesTarget_iff_kernel_inclusion
#print axioms pairBlind_downward

end NewMathDiscovery.LinearBlindness
