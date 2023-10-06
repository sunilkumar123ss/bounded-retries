"""Deterministic retry policy with injectable operation and sleep functions."""
import argparse
import json
import math
from pathlib import Path

class TransientError(Exception): pass
class PermanentError(Exception): pass
class RetryExhausted(Exception): pass


def retry(operation, sleep, max_attempts=4, base_delay=0.25, max_delay=2.0, delay_budget=5.0):
    if isinstance(max_attempts,bool) or not isinstance(max_attempts,int) or not 1 <= max_attempts <= 100:
        raise ValueError("max_attempts must be an integer from 1 to 100")
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x < 0 for x in (base_delay,max_delay,delay_budget)):
        raise ValueError("delay settings must be finite and nonnegative")
    if max_delay < base_delay:
        raise ValueError("max_delay must be at least base_delay")
    waited=0.0
    for attempt in range(1,max_attempts+1):
        try:
            return {"value":operation(), "attempts":attempt, "scheduled_delay":waited}
        except TransientError as exc:
            if attempt == max_attempts:
                raise RetryExhausted(f"attempt budget exhausted after {attempt} calls") from exc
            delay=min(max_delay,base_delay*2**(attempt-1))
            if waited+delay > delay_budget:
                raise RetryExhausted(f"delay budget exhausted after {attempt} calls") from exc
            sleep(delay)
            waited+=delay


def simulate(outcomes, **settings):
    if not isinstance(outcomes,list) or not outcomes or any(x not in {"success","transient","permanent"} for x in outcomes):
        raise ValueError("outcomes must be a nonempty list of success/transient/permanent")
    calls=0
    def operation():
        nonlocal calls
        outcome=outcomes[min(calls,len(outcomes)-1)]
        calls+=1
        if outcome == "transient":raise TransientError("synthetic temporary failure")
        if outcome == "permanent":raise PermanentError("synthetic non-retryable failure")
        return "synthetic tool result"
    delays=[]
    try:
        return {"status":"success", **retry(operation,delays.append,**settings), "delays":delays}
    except (RetryExhausted,PermanentError) as exc:
        return {"status":"failed", "reason":str(exc), "attempts":calls, "delays":delays}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan",type=Path,default=Path(__file__).with_name("plan.json"))
    parser.add_argument("--attempts",type=int,default=4)
    parser.add_argument("--delay-budget",type=float,default=5)
    args=parser.parse_args()
    try:result=simulate(json.loads(args.plan.read_text()),max_attempts=args.attempts,delay_budget=args.delay_budget)
    except (ValueError,OSError,TypeError) as exc:parser.error(str(exc))
    print(json.dumps(result,indent=2))
    if result["status"] != "success":raise SystemExit(1)

if __name__ == "__main__":main()
