import { BalanceHeader } from '../components/BalanceHeader';
import { EmptyState } from '../components/ui/EmptyState';

export function PlayPage() {
  return (
    <div>
      <div className="mb-8">
        <BalanceHeader />
      </div>
      <EmptyState
        title="Pick a stat to start"
        subline="Markets, the wager slip, and matchmaking arrive in Phase 3."
      />
    </div>
  );
}
