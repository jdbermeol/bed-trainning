
class Applicant(object):

    def is_credible(self):
        return True

    def get_credit_score(self):
        return 700

    def get_employment_years(self):
        return 10

    def has_criminal_record(self):
        return True


class Evaluator(object):

    def evaluate(self, applicant):
        raise Exception("Not implemented")


class QualifiedEvaluator(Evaluator):

    def evaluate(self, applicant):
        return applicant.is_credible()


class EvaluatorChain(Evaluator):

    def __init__(self, next_evaluator):
        self.next_evaluator = next_evaluator

    def evaluate(self, applicant):
        return self.next_evaluator.evaluate(applicant)


class CreditEvaluator(EvaluatorChain):

    def evaluate(self, applicant):
        if applicant.get_credit_score() > 600:
            return super(CreditEvaluator, self).evaluate(applicant)
        else:
            return False


class EmploymentEvaluator(EvaluatorChain):

    def evaluate(self, applicant):
        if applicant.get_employment_years() > 0:
            return super(EmploymentEvaluator, self).evaluate(applicant)
        else:
            return False


class CriminalRecordsEvaluator(EvaluatorChain):

    def evaluate(self, applicant):
        if not applicant.has_criminal_record():
            return super(CriminalRecordsEvaluator, self).evaluate(applicant)
        else:
            return False


def evaluate(applicant, evaluator):
    result = "accepted" if evaluator.evaluate(applicant) else "rejected"
    print("Result of evaluating applicant: %s" % (result,))


def evaluate_fun(applicant, evaluator):
    result = "accepted" if applicant.is_credible() and evaluator(applicant) else "rejected"
    print("Result of evaluating applicant: %s" % (result,))


def _and(*predicates):
    def _joined_predicate(target):
        return all(map(lambda p: p(target), predicates))
    return _joined_predicate


if __name__ == "__main__":
    applicant = Applicant()

    # evaluate(applicant, CreditEvaluator(QualifiedEvaluator()))
    # evaluate(applicant, CreditEvaluator(EmploymentEvaluator(QualifiedEvaluator())))
    # evaluate(applicant, CriminalRecordsEvaluator(EmploymentEvaluator(QualifiedEvaluator())))
    # evaluate(applicant, CriminalRecordsEvaluator(CreditEvaluator(EmploymentEvaluator(QualifiedEvaluator()))))

    credit_evaluator = lambda applicant: applicant.get_credit_score() > 600
    employment_evaluator = lambda applicant: applicant.get_employment_years() > 0
    criminal_record_evaluator = lambda applicant: not applicant.has_criminal_record()

    evaluate_fun(applicant, credit_evaluator)
    evaluate_fun(applicant, _and(credit_evaluator, employment_evaluator))
    evaluate_fun(applicant, _and(criminal_record_evaluator, employment_evaluator))
    evaluate_fun(applicant, _and(criminal_record_evaluator, credit_evaluator, employment_evaluator))
