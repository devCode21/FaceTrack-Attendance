
export const Card = ({ children, className }) => (
  <div
    className={`rounded-2xl border border-zinc-800 bg-zinc-900/60 backdrop-blur-xl shadow-[0_0_25px_rgba(0,0,0,0.45)] p-10 w-full max-w-md ${className}`}
  >
    {children}
  </div>
);

export const CardHeader = ({ children }) => <div className="flex flex-col space-y-1.5">{children}</div>;

export const CardTitle = ({ children }) => (
  <h3 className="text-3xl font-semibold leading-none tracking-tight text-neutral-100">{children}</h3>
);

export const CardDescription = ({ children }) => (
  <p className="text-sm text-neutral-400 mt-1">{children}</p>
);

export const CardContent = ({ children }) => <div className="pt-6">{children}</div>;

// Input + Icon Field
export const Input = ({ type = "text", ...props }) => (
  <input
    type={type}
    {...props}
    className={`flex h-11 w-full rounded-lg border border-zinc-700 bg-zinc-900/70 text-neutral-200 px-3 py-2 text-sm shadow-inner placeholder:text-neutral-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400 focus-visible:border-sky-400 transition ${props.className}`}
  />
);

export const Button = ({ children, className, ...props }) => (
  <button
    {...props}
    className={`inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all h-11 px-4 py-2 bg-sky-600 text-white hover:bg-sky-700 shadow-lg hover:scale-[1.02] disabled:opacity-50 disabled:pointer-events-none ${className}`}
  >
    {children}
  </button>
);

// Toast (mock)


// Label + Icon Input Wrapper
export const LabeledInput = ({ Icon, label, id, error, ...props }) => (
  <div className="space-y-1">
    <label htmlFor={id} className="text-sm font-medium text-neutral-300">
      {label}
    </label>
    <div className="relative">
      <Input id={id} className={`pl-10 ${error ? "border-red-500 ring-red-500" : ""}`} {...props} />
      <Icon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-neutral-500" />
    </div>
    {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
  </div>
);