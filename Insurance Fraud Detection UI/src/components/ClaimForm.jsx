import { useState } from 'react';
import { FiSearch, FiLoader } from 'react-icons/fi';

const claimTypes = ['Select Claim Type', 'Auto', 'Medical', 'Property', 'Liability', 'Disability'];
const policyTypes = ['Select Policy Type', 'Basic', 'Standard', 'Premium', 'Comprehensive'];
const states = ['Select State', 'CA', 'TX', 'NY', 'FL', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'];
const claimStatuses = ['Select Claim Status', 'Approved', 'Denied', 'Under Review', 'Closed'];

export default function ClaimForm({ onSubmit, isLoading }) {
    const [formData, setFormData] = useState({
        claim_amount: '',
        claimant_age: '',
        policy_duration_days: '',
        previous_claims: '',
        claim_type: '',
        policy_type: '',
        state: '',
        claim_status: '',
        days_since_policy_start: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    const fields = [
        {
            name: 'claim_amount',
            label: 'Claim Amount ($)',
            type: 'number',
            placeholder: 'e.g. 25000',
            span: true,
        },
        {
            name: 'claimant_age',
            label: 'Claimant Age',
            type: 'number',
            placeholder: 'e.g. 35',
        },
        {
            name: 'previous_claims',
            label: 'Previous Claims',
            type: 'number',
            placeholder: 'e.g. 2',
        },
        {
            name: 'claim_type',
            label: 'Claim Type',
            type: 'select',
            options: claimTypes,
        },
        {
            name: 'policy_type',
            label: 'Policy Type',
            type: 'select',
            options: policyTypes,
        },
        {
            name: 'state',
            label: 'State',
            type: 'select',
            options: states,
        },
        {
            name: 'claim_status',
            label: 'Claim Status',
            type: 'select',
            options: claimStatuses,
        },
        {
            name: 'policy_duration_days',
            label: 'Policy Duration (days)',
            type: 'number',
            placeholder: 'e.g. 365',
        },
        {
            name: 'days_since_policy_start',
            label: 'Days Since Policy Start',
            type: 'number',
            placeholder: 'e.g. 180',
        },
    ];

    return (
        <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid gap-5 sm:grid-cols-2">
                {fields.map((field) => (
                    <div key={field.name} className={field.span ? 'sm:col-span-2' : ''}>
                        <label className="block text-sm font-medium text-dark-300 mb-2">
                            {field.label}
                        </label>
                        {field.type === 'select' ? (
                            <div className="relative">
                                <select
                                    name={field.name}
                                    value={formData[field.name]}
                                    onChange={handleChange}
                                    required
                                    className="select-field"
                                >
                                    {field.options.map((opt) => (
                                        <option key={opt} value={opt === field.options[0] ? '' : opt} disabled={opt === field.options[0]}>
                                            {opt}
                                        </option>
                                    ))}
                                </select>
                                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                                    <svg className="h-4 w-4 text-dark-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                    </svg>
                                </div>
                            </div>
                        ) : (
                            <input
                                type={field.type}
                                name={field.name}
                                value={formData[field.name]}
                                onChange={handleChange}
                                placeholder={field.placeholder}
                                required
                                min={field.name === 'claimant_age' ? 18 : field.name === 'claim_amount' ? 1 : 0}
                                className="input-field"
                            />
                        )}
                    </div>
                ))}
            </div>

            <button
                type="submit"
                disabled={isLoading}
                className="w-full btn-primary flex items-center justify-center gap-3 text-lg mt-6 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0"
            >
                {isLoading ? (
                    <>
                        <FiLoader className="w-5 h-5 animate-spin" />
                        Analyzing Claim…
                    </>
                ) : (
                    <>
                        <FiSearch className="w-5 h-5" />
                        Predict Fraud
                    </>
                )}
            </button>
        </form>
    );
}
