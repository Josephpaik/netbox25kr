/**
 * `StateManger` configuration options.
 */
interface StateOptions {
  /**
   * If true, all values will be written to localStorage when calling `set()`. Additionally, when
   * a new state instance is initialized, if the same localStorage state key (see `key` property)
   * exists in localStorage, the value will be read and used as the initial value.
   */
  persist?: boolean;

  /**
   * Use a static localStorage key instead of automatically generating one.
   */
  key?: string;

  /**
   * Optional encryption key for encrypting/decrypting state data.
   * If omitted, a built-in default key will be used.
   */
  encryptionKey?: string;
}

/**
 * Typed implementation of native `ProxyHandler`.
 */
class ProxyStateHandler<T extends Dict, K extends keyof T = keyof T> implements ProxyHandler<T> {
  public set<S extends Index<T, K>>(target: T, key: S, value: T[S]): boolean {
    target[key] = value;
    return true;
  }

  public get<G extends Index<T, K>>(target: T, key: G): T[G] {
    return target[key];
  }
  public has(target: T, key: string): boolean {
    return key in target;
  }
}

/**
 * Manage runtime and/or locally stored (via localStorage) state.
 */
export class StateManager<T extends Dict, K extends keyof T = keyof T> {
  /**
   * implemented `ProxyHandler` for the underlying `Proxy` object.
   */
  private handlers: ProxyStateHandler<T>;
  /**
   * Underlying `Proxy` object for this instance.
   */
  private proxy: T;
  /**
   * Options for this instance.
   */
  private options: StateOptions;
  /**
   * localStorage key for this instance.
   */
  private key: string = '';
  /**
   * Encryption key used for localStorage encryption.
   */
  private encryptionKey: string = '';

  constructor(raw: T, options: StateOptions) {
    this.options = options;

    // Use static key if defined.
    if (typeof this.options.key === 'string') {
      this.key = this.options.key;
    } else {
      this.key = this.generateStateKey(raw);
    }

    // Use provided encryption key or default to a built-in value.
    if (typeof this.options.encryptionKey === 'string' && this.options.encryptionKey.length > 0) {
      this.encryptionKey = this.options.encryptionKey;
    } else {
      // WARNING: In production, use a unique per-user key that's never checked-in to source control.
      this.encryptionKey = 'netbox-encryption-default-key-please-change';
    }

    if (this.options.persist) {
      const saved = this.retrieve();
      if (saved !== null) {
        raw = { ...raw, ...saved };
      }
    }

    this.handlers = new ProxyStateHandler<T>();
    this.proxy = new Proxy(raw, this.handlers);

    if (this.options.persist) {
      this.save();
    }
  }

  /**
   * Encrypt a string using AES-GCM and a provided key.
   */
  private async encrypt(plainText: string): Promise<string> {
    // Convert the password to a key.
    const enc = new TextEncoder();
    const password = enc.encode(this.encryptionKey);
    const salt = window.crypto.getRandomValues(new Uint8Array(16));
    const keyMaterial = await window.crypto.subtle.importKey(
      "raw", password, "PBKDF2", false, ["deriveKey"]
    );
    const key = await window.crypto.subtle.deriveKey(
      {
        "name": "PBKDF2",
        salt: salt,
        iterations: 100000,
        hash: "SHA-256"
      },
      keyMaterial,
      { "name": "AES-GCM", "length": 256 },
      false,
      ["encrypt"]
    );
    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    const encrypted = await window.crypto.subtle.encrypt(
      { name: "AES-GCM", iv: iv },
      key,
      enc.encode(plainText)
    );
    // Concatenate salt, iv, and ciphertext for storage
    const buffer = new Uint8Array(salt.length + iv.length + encrypted.byteLength);
    buffer.set(salt, 0);
    buffer.set(iv, salt.length);
    buffer.set(new Uint8Array(encrypted), salt.length + iv.length);
    return window.btoa(String.fromCharCode(...buffer));
  }

  /**
   * Decrypt a string using AES-GCM and a provided key.
   */
  private async decrypt(encrypted: string): Promise<string> {
    const buffer = Uint8Array.from(atob(encrypted), c => c.charCodeAt(0));
    const salt = buffer.slice(0, 16);
    const iv = buffer.slice(16, 28);
    const ciphertext = buffer.slice(28);
    const enc = new TextEncoder();
    const password = enc.encode(this.encryptionKey);
    const keyMaterial = await window.crypto.subtle.importKey(
      "raw", password, "PBKDF2", false, ["deriveKey"]
    );
    const key = await window.crypto.subtle.deriveKey(
      {
        "name": "PBKDF2",
        salt: salt,
        iterations: 100000,
        hash: "SHA-256"
      },
      keyMaterial,
      { "name": "AES-GCM", "length": 256 },
      false,
      ["decrypt"]
    );
    const decrypted = await window.crypto.subtle.decrypt(
      { name: "AES-GCM", iv: iv },
      key,
      ciphertext
    );
    return new TextDecoder().decode(decrypted);
  }

  /**
   * Generate a semi-unique localStorage key for this instance.
   */
  private generateStateKey(obj: T): string {
    const encoded = window.btoa(Object.keys(obj).join('---'));
    return `netbox-${encoded}`;
  }

  /**
   * Get the current value of `key`.
   *
   * @param key Object key name.
   * @returns Object value.
   */
  public get<G extends Index<T, K>>(key: G): T[G] {
    return this.handlers.get(this.proxy, key);
  }

  /**
   * Set a new value for `key`.
   *
   * @param key Object key name.
   * @param value New value.
   */
  public set<G extends Index<T, K>>(key: G, value: T[G]): void {
    this.handlers.set(this.proxy, key, value);
    if (this.options.persist) {
      this.save();
    }
  }

  /**
   * Access the full instance.
   *
   * @returns StateManager instance.
   */
  public all(): T {
    return this.proxy;
  }

  /**
   * Access all state keys.
   */
  public keys(): K[] {
    return Object.keys(this.proxy) as K[];
  }

  /**
   * Access all state values.
   */
  public values(): T[K][] {
    return Object.values(this.proxy) as T[K][];
  }

  /**
   * Serialize and save the current state to localStorage.
   */
  private async save(): Promise<void> {
    const value = JSON.stringify(this.proxy);
    const encrypted = await this.encrypt(value);
    localStorage.setItem(this.key, encrypted);
  }

  /**
   * Retrieve the serialized state object from localStorage.
   *
   * @returns Parsed state object.
   */
  private async retrieve(): Promise<T | null> {
    const raw = localStorage.getItem(this.key);
    if (raw !== null) {
      try {
        const decrypted = await this.decrypt(raw);
        const data = JSON.parse(decrypted) as T;
        return data;
      } catch (e) {
        // fall back to null if decryption fails
        return null;
      }
    }
    return null;
  }
}

/**
 * Create a new state object. Only one instance should exist at runtime for a given state.
 *
 * @param initial State's initial value.
 * @param options State management instance options.
 * @returns State management instance.
 */
export function createState<T extends Dict>(
  initial: T,
  options: StateOptions = {},
): StateManager<T> {
  return new StateManager<T>(initial, options);
}
