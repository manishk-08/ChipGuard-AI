"use client";

import { useState } from "react";
import { Upload, AlertTriangle, Shield, Download } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await fetch("/api/boms/upload", { method: "POST", body: form });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error("Upload failed", e);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <header className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Shield className="w-8 h-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">ChipGuard AI</h1>
        </div>
        <p className="text-gray-600">BOM risk and compliance intelligence for electronics teams</p>
      </header>

      <section className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Upload className="w-5 h-5 text-blue-600" />
          Upload Bill of Materials
        </h2>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <p className="text-sm text-gray-400 mt-2">CSV or XLSX files supported</p>
        </div>
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {uploading ? "Processing..." : "Analyze BOM"}
        </button>
      </section>

      {result && (
        <section className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-yellow-500" />
            Risk Report: {result.name}
          </h2>
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="bg-green-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-green-700">{result.items?.length || 0}</div>
              <div className="text-sm text-green-600">Components</div>
            </div>
            <div className="bg-yellow-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-yellow-700">--</div>
              <div className="text-sm text-yellow-600">At Risk</div>
            </div>
            <div className="bg-red-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-red-700">--</div>
              <div className="text-sm text-red-600">Compliance Flags</div>
            </div>
          </div>
          <div className="flex gap-3">
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-sm">
              <Download className="w-4 h-4" />
              Export PDF Report
            </button>
          </div>
        </section>
      )}

      <footer className="text-xs text-gray-400 text-center border-t border-gray-200 pt-4 mt-8">
        <p className="mb-1">ChipGuard AI &mdash; Decision-support only. Not legal advice.</p>
        <p>Consult a qualified trade compliance professional for final determinations.</p>
      </footer>
    </div>
  );
}
